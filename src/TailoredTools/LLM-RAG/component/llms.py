from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from component.embedding import Zhipuembedding, BGEembedding
from component.data_chunker import ReadFile
from component.databases import Vectordatabase
import os
import json
from typing import Dict, List, Optional, Tuple, Union
import PyPDF2
from openai import OpenAI

class Openai_model:
    def __init__(self, api_key: str, base_url: str, embedding_model, model_name: str = 'deepseek-chat', temperature: float = 1, software: str = "hadoop") -> None:

        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.client = OpenAI(api_key="your apikey", base_url="https://api.deepseek.com")
        self.temperature = temperature
        self.software = software


    
        self.db = Vectordatabase(path = f'./RAG/ragdemo/tinyRAG/database/{self.software}')
        self.db.load_vector()
        self.embedding_model = embedding_model

    def chat(self, configuration1: str, configurationlist: str):
        configurationlist = ", ".join(configurationlist) if isinstance(configurationlist, list) else str(configurationlist)
        template = """Use the above context to answer the question. You are an expert in analyzing dependency relationships between configurations. Your task is to determine if there are any dependencies between a given Configuration (Configuration 1) and a list of other Configurations, describe the dependency using BNF and classify these dependencies according to the provided rules.

        The BNF grammar you should follow to describe the configuration
        dependencies is as follows:

        <Dependency> ::= <Condition> => <ConstraintItem>
        <Condition> ::= <Variable> <Relation> <ValueExpression>
        <ConstraintItem> ::= <Variable> <Relation> <ValueExpression>
        <Relation> ::= "=" | "!=" | "in" | "not in" | ">" | "<"
        <ValueExpression> ::= <SingleValue> | <ValueSet> | <ValueRange> | <Expression>
        <SingleValue> ::= <Number> | <Boolean> | <String> | "null" | “ANY"
        <ValueSet> ::= {{ <SingleValue> ("," <SingleValue>)* }}
        <ValueRange> ::= [ <Number> ".." <Number> ]
        <Expression> ::= <Term> ( ("+" | "-") <Term> )*
        <Term> ::= <Factor> ( ("*" | "/") <Factor> )*
        <Factor> ::= <Number> | <Variable> | "(" <Expression> ")"

        Explanation of Importance
        <Variable> : A configuration parameter.
        "ANY": [default.MIN_VALUE .. default.MAX_VALUE].

        Determine the corresponding classification based on the generated BNF

        Dependency Type	Expression Pattern (Simplified)	Meaning
        Default	A=ANY or null => B=A	A determines the default value of B
        Control	A specific value or true => B is valid and non-null	A enables/activates B
        Overwrite	A!=null => B=ANY/invalid	A overrides the effect of B
        Value	A numerical comparison B => must satisfy a specific size relationship	A and B have a numerical constraint relationship
        Behavioral	All other types	Other types

        Pay attention not to provide content other than in JSON format.
        Output json format:
        [
        {{
            "Configuration A": "The parameter name that has a dependency relationship with Configuration B",
            "Configuration B": "The parameter name that has a dependency relationship with Configuration A",
            "Type": "The classification result of the dependency (Control/Default/Overwrite/Value/Behavioral)",
            "BNF": "Descript the dependency in BNF formula."
        }},
        {{
            "Configuration A": "The parameter name with a dependency relationship",
            "Configuration B": "Another parameter name with a dependency relationship",
            "Type": "The classification result of the dependency",
            "BNF": "Descript the dependency in BNF formula."
        }}
        // There may be multiple such objects depending on how many parameters have a dependency relationship with Configuration 1，if there's not dependency , don't output anything, just pass.
        ]
        Configuration 1:[{configuration1}]

        Reference context of Configuration 1: [{info}]
        
        Configuration list: [{configurationlist}]
        """



        info = self.db.query(configuration1, self.embedding_model, 1)
        
        prompt = template.format(configuration1=configuration1, info=info, configurationlist =configurationlist)
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=False
        )

        res = response.choices[0].message.content
        return res
package ldsa;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.AssignExpr;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.NameExpr;

import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;

public class varsearch {

    static class TaintRecord {
        String variable;
        int line;
        String filepath;
        String from;

        TaintRecord(String variable, int line, String filepath, String from) {
            this.variable = variable;
            this.line = line;
            this.filepath = filepath;
            this.from = from;
        }

        @Override
        public String toString() {
            return filepath + " " + line + " " + variable + " " + from;
        }
    }

    private static final Set<String> tainted = new HashSet<>();
    private static final List<TaintRecord> results = new ArrayList<>();
    private static final int maxDepth = 6;

    public static void main(String[] args) throws IOException {
        String filePath = "your java file path";
        String seedVariable = "your variable name";

        analyzeFile(filePath, seedVariable);
        writeResult("TAresult.txt");
    }

    public static void analyzeFile(String filePath, String seedVariable) throws IOException {
        FileInputStream in = new FileInputStream(filePath);
        JavaParser parser = new JavaParser();
        ParseResult<CompilationUnit> result = parser.parse(in);

        if (!result.isSuccessful() || !result.getResult().isPresent()) {
            System.err.println("Failed to parse: " + filePath);
            return;
        }

        CompilationUnit cu = result.getResult().get();

        cu.findAll(NameExpr.class).forEach(expr -> {
            if (expr.getNameAsString().equals(seedVariable)) {
                int line = expr.getBegin().map(p -> p.line).orElse(-1);
                if (tainted.add(seedVariable)) {
                    results.add(new TaintRecord(seedVariable, line, filePath, "SOURCE"));
                }
            }
        });

        cu.findAll(VariableDeclarator.class).forEach(vd -> {
            if (vd.getNameAsString().equals(seedVariable)) {
                int line = vd.getBegin().map(p -> p.line).orElse(-1);
                if (tainted.add(seedVariable)) {
                    results.add(new TaintRecord(seedVariable, line, filePath, "SOURCE"));
                }
            }
        });

        propagateTaint(cu, filePath, seedVariable, 1);
    }

    private static void propagateTaint(CompilationUnit cu, String filePath, String variable, int depth) {
        if (depth > maxDepth) return;

        cu.findAll(AssignExpr.class).forEach(assign -> {
            Expression rhs = assign.getValue();
            Expression lhs = assign.getTarget();

            if (rhsUsesVariable(rhs, variable) && lhs.isNameExpr()) {
                String newVar = lhs.asNameExpr().getNameAsString();
                int line = assign.getBegin().map(p -> p.line).orElse(-1);
                if (tainted.add(newVar)) {
                    results.add(new TaintRecord(newVar, line, filePath, variable));
                    propagateTaint(cu, filePath, newVar, depth + 1);
                }
            }
        });

        cu.findAll(VariableDeclarator.class).forEach(vd -> {
            Optional<Expression> init = vd.getInitializer();
            if (init.isPresent() && rhsUsesVariable(init.get(), variable)) {
                String newVar = vd.getNameAsString();
                int line = vd.getBegin().map(p -> p.line).orElse(-1);
                if (tainted.add(newVar)) {
                    results.add(new TaintRecord(newVar, line, filePath, variable));
                    propagateTaint(cu, filePath, newVar, depth + 1);
                }
            }
        });
    }

    private static boolean rhsUsesVariable(Expression rhs, String variable) {
        return rhs.findAll(NameExpr.class).stream()
                .anyMatch(expr -> expr.getNameAsString().equals(variable));
    }

    private static void writeResult(String outFile) throws IOException {
        try (PrintWriter writer = new PrintWriter(new FileWriter(outFile))) {
            for (TaintRecord r : results) {
                System.out.println(r);
                writer.println(r);
            }
        }
        System.out.println("Taint propagation completed. Results written to: " + outFile);
    }
}
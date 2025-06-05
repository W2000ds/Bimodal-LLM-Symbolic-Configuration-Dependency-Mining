import pkg_resources
import subprocess

subprocess.check_call(["pip", "install", "-r", "requirements.txt"])


with open("requirements.txt", "r") as f:
    packages = f.readlines()
packages = [pkg.strip() for pkg in packages]


with open("version_info.txt", "w") as output_file:
    for pkg in packages:
        if pkg == "" or pkg.startswith("#"):  
            continue
        try:
           
            version = pkg_resources.get_distribution(pkg).version
            output_file.write(f"{pkg}=={version}\n")
        except pkg_resources.DistributionNotFound:
            
            output_file.write(f"{pkg}: Not Found\n")

print("version_info.txt done.")
import re
import sys
import logging
import  os.path, subprocess
from subprocess import STDOUT, PIPE
from flask import Flask, request, jsonify
from flask_cors import CORS

# create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler for logging to a file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

app = Flask(__name__)
CORS(app)


'''
this is the handler for a post request to run java code
'''
@app.route('/run-java', methods=["POST"])
def run_java():
    java_code = request.json.get("java_code")
    input_text = request.json.get("input_text")

    result = execute_java_code(java_code, input_text)
    return jsonify({
        'statusCode': 200,
        'body': result
    })


'''
logic for running java code using python
'''
def execute_java_code(code, input_args):
    input_args = input_args.split("\n")
    logger.info(input_args)
    logger.info(type(input_args))

    # extract className from code
    class_names = re.findall(r'class\s+([A-Za-z_][A-Za-z0-9_]*)\s*{', code)

    # write the code in a file
    file_path = class_names[0]+".java"
    with open(file_path, "w") as java_file:
        java_file.write(code)

    # compile the java code first
    result_body = ""
    compile_process = subprocess.run(['javac', file_path], capture_output=True, text=True)
    logger.info(compile_process.returncode)

    if compile_process.returncode == 0:
        # Run the compiled Java code
        run_process = subprocess.run(["java", file_path], capture_output=True, text=True, input="\n".join(input_args))
        if run_process.returncode == 0:
            logger.info("Java code executed successfully:")
            logger.info(run_process.stdout)
            result_body = run_process.stdout
        else:
            logger.error("Error running java code:")
            logger.error(run_process.stderr)
            result_body = run_process.stderr
    else:
        logger.error("Error compiling java code")
        logger.error(compile_process.stderr)
        result_body = compile_process.stderr

    # remove the java file
    if os.path.exists(class_names[0]+".java"):
        os.remove(class_names[0]+".java")
    if os.path.exists(class_names[0]+".class"):
        os.remove(class_names[0]+".class")


    logger.info(result_body)

    return result_body

'''
run the python server
'''
if __name__ == "__main__":
    app.run(debug=True)

# def handler(event, context):
#     # language = event.get('language','python')
#     # code = event.get('code','')
#     language = "java"
#     code = """
#     import java.util.Scanner;

#     public class MyClass {
#         public static void main(String[] args) {
#             Scanner scanner = new Scanner(System.in);

#             System.out.println("Hello All of y'all motherfuckers!!");
#             String name = scanner.nextLine();
#             int age = scanner.nextInt();
#             System.out.print("Hello "+name+" "+age);
#         }
#     }"""

#     # if language == 'python':
#     #     result = execute_python_code(code)
#     if language == 'java':
#         input_text = ['Avinash','23']
#         result = execute_java_code(code, input_text)
#     # elif language == 'cpp':
#     #     result = execute_cpp_code(code)
#     else:
#         result = 'Unsupported language!'

#     return {
#         'statusCode': 200,
#         'body': result
#     }



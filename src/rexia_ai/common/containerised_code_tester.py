"""Containerised Code Tester class for ReXia.AI"""

import docker
import tempfile
import ast
import os
import inspect
import json
import traceback
import textwrap
from typing import Any, List, Dict, Tuple, Union

class ContainerisedCodeTester:
    """
    A class for executing Python code in isolated Docker containers.
    This class provides functionality to run Python code and associated tests
    in a controlled Docker environment, ensuring security and consistency.
    """

    def __init__(self, image: str = "python:3.12-slim", timeout: int = 30):
        """
        Initialize the ContainerisedCodeExecutor.

        Args:
            image (str): The Docker image to use. Defaults to "python:3.12-slim".
            timeout (int): The execution timeout in seconds. Defaults to 30.

        Raises:
            RuntimeError: If the Docker client fails to initialize.
        """
        try:
            self.client = docker.from_env()
            print(f"Docker client initialized successfully.")
        except docker.errors.DockerException as e:
            error_msg = f"Failed to initialize Docker client: {str(e)}"
            print(error_msg)
            raise RuntimeError(error_msg)
        self.image = image
        self.timeout = timeout
        print(f"ContainerisedCodeExecutor initialized with image: {image}, timeout: {timeout}s")

    def execute_code(self, code: Union[str, List[str]], test_class: type) -> Dict[str, Any]:
        """
        Execute the provided code and test class in a Docker container.

        Args:
            code (Union[str, List[str]]): The Python code to execute, either as a string or a list of strings.
            test_class (type): The test class to run against the code.

        Returns:
            Dict[str, Any]: A dictionary containing the execution results.
        """
        try:
            if isinstance(code, list):
                code = "\n".join(code)

            with tempfile.TemporaryDirectory() as tmpdir:
                print(f"Created temporary directory: {tmpdir}")
                self._write_files(tmpdir, code, test_class)
                status_code, stdout, stderr = self._run_container(tmpdir)
                
                if not stdout and not stderr:
                    print("No output from container")
                else:
                    print("Container produced output")
                    print(f"Stdout length: {len(stdout)} characters")
                    print(f"Stderr length: {len(stderr)} characters")
                
                print(f"Container execution completed with status code: {status_code}")
                
                results = self._parse_output(status_code, stdout, stderr)

                if results.get("all_passed"):
                    print("All tests passed successfully!")
                else:
                    print("Some tests failed or errors occurred.")
                    print(f"Passed tests: {len(results['passed'])}")
                    print(f"Failed tests: {len(results['failed'])}")
                    print(f"Errors: {len(results['errors'])}")

                return results

        except Exception as e:
            error_message = f"An error occurred during code execution: {str(e)}"
            print(error_message)
            traceback.print_exc()
            return {
                "error": error_message,
                "all_passed": False,
                "passed": [],
                "failed": [],
                "errors": [{"type": type(e).__name__, "message": str(e)}]
            }

    def _write_files(self, tmpdir: str, code: str, test_class: type) -> None:
        """
        Write the code and test files to a temporary directory.

        Args:
            tmpdir (str): Path to the temporary directory.
            code (str): The Python code to write.
            test_class (type): The test class to write.
        """
        code_path = os.path.join(tmpdir, "code.py")
        test_path = os.path.join(tmpdir, "test.py")
        main_path = os.path.join(tmpdir, "main.py")
        
        # Parse the code to find the function name
        tree = ast.parse(code)
        function_def = next((node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)), None)
        if function_def is None:
            raise ValueError("No function definition found in the provided code.")
        function_name = function_def.name

        with open(code_path, "w") as f:
            f.write(code)
        print(f"Written code to: {code_path}")
        
        with open(test_path, "w") as f:
            f.write(inspect.getsource(test_class))
        print(f"Written test class to: {test_path}")
        
        main_content = self._generate_main_test_logic(test_class.__name__, function_name)
        with open(main_path, "w") as f:
            f.write(main_content)
        print(f"Written main execution logic to: {main_path}")

    def _run_container(self, tmpdir: str) -> Tuple[int, str, str]:
        """
        Run the Docker container with the provided code and tests.

        Args:
            tmpdir (str): Path to the temporary directory containing the code and test files.

        Returns:
            Tuple[int, str, str]: A tuple containing the exit status code, stdout, and stderr.

        Raises:
            RuntimeError: If there's an error running the container.
        """
        try:
            print(f"Starting container with image: {self.image}")
            container = self.client.containers.run(
                self.image,
                command=["python", "/app/main.py"],
                volumes={tmpdir: {"bind": "/app", "mode": "ro"}},
                working_dir="/app",
                detach=True,
                mem_limit="128m",
                cpu_quota=50000,
                network_mode="none",
            )

            print(f"Container started. Waiting for completion...")
            result = container.wait(timeout=self.timeout)
            stdout = container.logs(stdout=True, stderr=False).decode("utf-8")
            stderr = container.logs(stdout=False, stderr=True).decode("utf-8")
            return result["StatusCode"], stdout, stderr
        except Exception as e:
            print(f"Error in _run_container: {str(e)}")
            return 1, "", str(e)
        finally:
            try:
                container.remove(force=True)
                print("Container removed.")
            except:
                print("Failed to remove container.")

    @staticmethod
    def _generate_main_test_logic(class_name: str, func_name: str) -> str:
        """
        Generate the main test execution logic as a string.

        Args:
            class_name (str): The name of the test class.
            func_name (str): The name of the function to be tested.

        Returns:
            str: A string containing the main test execution logic.
        """
        return textwrap.dedent(f'''
            import sys
            import json
            import traceback
            import inspect

            from code import {func_name}
            from test import {class_name}

            def run_tests():
                test_class = {class_name}
                results = {{"passed": [], "failed": [], "errors": [], "output": []}}

                def log(message):
                    results["output"].append(message)
                    print(message)

                log("Starting test execution...")

                func_to_test = {func_name}

                # Run setUpClass
                try:
                    test_class.setUpClass()
                except Exception as e:
                    log(f"Error in setUpClass: {{str(e)}}")
                    results["errors"].append({{
                        "type": type(e).__name__,
                        "message": str(e),
                        "details": traceback.format_exc()
                    }})
                    return results

                for method_name, method in inspect.getmembers(test_class, predicate=lambda m: inspect.ismethod(m) and m.__self__ is test_class):
                    if method_name.startswith('test_'):
                        log(f"Running test method: {{method_name}}")
                        try:
                            method(func_to_test)
                            results["passed"].append(method_name)
                            log(f"Test passed: {{method_name}}")
                        except AssertionError as e:
                            log(f"Test failed: {{method_name}}, Error: {{str(e)}}")
                            results["failed"].append({{
                                "name": method_name,
                                "error": str(e),
                                "details": traceback.format_exc()
                            }})
                        except Exception as e:
                            log(f"Test error: {{method_name}}, Error: {{str(e)}}")
                            results["errors"].append({{
                                "type": type(e).__name__,
                                "message": str(e),
                                "details": traceback.format_exc()
                            }})
                
                log("Finished running all tests")
                return results

            if __name__ == '__main__':
                test_results = run_tests()
                print("--- BEGIN JSON RESULTS ---")
                print(json.dumps(test_results, indent=2))
                print("--- END JSON RESULTS ---")
                sys.exit(1 if test_results["failed"] or test_results["errors"] else 0)
        ''')

    @staticmethod
    def _parse_output(status_code: int, stdout: str, stderr: str) -> Dict[str, Any]:
        """
        Parse the output from the container execution.

        Args:
            status_code (int): The exit status code of the container.
            stdout (str): The standard output from the container.
            stderr (str): The standard error from the container.

        Returns:
            Dict[str, Any]: A dictionary containing the parsed results.
        """
        results = {
            "all_passed": False,
            "passed": [],
            "failed": [],
            "errors": [],
            "stdout": stdout,
            "stderr": stderr,
        }

        if status_code != 0:
            results["errors"].append(f"Container exited with non-zero status code: {status_code}")

        try:
            json_start = stdout.find("--- BEGIN JSON RESULTS ---")
            json_end = stdout.find("--- END JSON RESULTS ---")
            
            if json_start != -1 and json_end != -1:
                json_str = stdout[json_start + len("--- BEGIN JSON RESULTS ---"):json_end].strip()
                print(f"Extracted JSON:\n{json_str}")
                
                test_results = json.loads(json_str)
                results["passed"] = test_results.get("passed", [])
                results["failed"] = test_results.get("failed", [])
                results["errors"].extend(test_results.get("errors", []))

                if results["passed"] and not results["failed"] and not results["errors"]:
                    results["all_passed"] = True
            else:
                raise ValueError("JSON markers not found in output")

        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse output as JSON: {str(e)}"
            print(error_msg)
            results["errors"].append(error_msg)
        except ValueError as e:
            error_msg = f"Error extracting JSON from output: {str(e)}"
            print(error_msg)
            results["errors"].append(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while parsing output: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            results["errors"].append(error_msg)

        return results
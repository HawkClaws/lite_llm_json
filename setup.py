from setuptools import setup, find_packages

with open("README.md", "r") as fp:
    readme = fp.read()

DESCRIPTION = "This library offers functionality to cleanly extract JSON from LLM responses and generate prompts for LLM that return JSON. It features a simple implementation while maintaining high versatility."

setup(
    name="LiteLLMJson",
    version="0.0.5",
    author="HawkClaws",
    packages=find_packages(),
    install_requires=[
        "jsonschema>=4.19.2"
    ],
    python_requires=">=3.6",
    include_package_data=True,
    url="https://github.com/HawkClaws/lite_llm_json",
    project_urls={"Source Code": "https://github.com/HawkClaws/lite_llm_json"},
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type='text/markdown',
    license="MIT",
)

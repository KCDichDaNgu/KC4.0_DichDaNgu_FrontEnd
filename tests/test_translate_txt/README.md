To run Automation Test:
1. Install
    - Install TestProject Agent: https://docs.testproject.io/getting-started/installation-and-setup
    - Register TestProject Agent
    - Run the agent locally before generating and running test case
2. Execution:
    - Open https://app.testproject.io/
    - Add below file to Open File to test.
        - Test login: 
        `tests/test_translate_txt/private/Test_Login-YbUa48JpXU-iWsKp9-GBkQ/package.yaml`
        - Test private translate txt:
        `tests/test_translate_txt/private/Test_Private_Translate_Txt-5LmvckxqM0qevBHS-MgVBg/package.yaml`
        - Test public translate txt: 
        `tests/test_translate_txt/public/Test_Translate_Txt-8LCTMbvzxEqBnVWTGwM6iQ/package.yaml`

    - During running process, use data from tests/test_translate_txt/input_files to upload file translation.
    
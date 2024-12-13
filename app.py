from flask import Flask, request, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)

# 预定义的用户和密码哈希
USERS = {
    # 'silicon':"scrypt:32768:8:1$5HBWGc5doFjgJXnn$5123dd177a269cefc9eee20a34a3f65ab8bbeab3e0d4cb2cfbcf2bd4510e390a12733a9d6ed304e1fb59816c2ce4a187a898addf02cbc567603ab561cc28436d",
    'silicon':f"{os.environ['silicon']}",
    # 'continue':"scrypt:32768:8:1$5MpfHuykL0gvutVt$1152a5f3f8da08d2ce5a81b12b3a6ab8034bc8f50486d59684c8511824d1ae3cbd2111974636fe6e784533fb7845b34f223b581e676cb5b3cc2f6e39272926d4",
    'continue':f"{os.environ['continue']}"
}

@app.route('/keys', methods=['GET'])
def protected():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        abort(401, description="Unauthorized: Bad credentials")
    if auth.username == "silicon":
        return os.environ['silicon_key']
    if auth.username == "continue":
        return jsonify({
        "models": [
            {
            "title": "deepseek-ai/DeepSeek-V2.5",
            "model": "deepseek-ai/DeepSeek-V2.5",
            "contextLength": 30000,
            "provider": "openai",
            "apiBase": "https://api.siliconflow.cn/v1",
            "apiKey": f"{os.environ['silicon']}",
            "requestOptions": {
                "extraBodyProperties": {
                "transforms": []
                }
            }
            },
            {
            "title": "Qwen/Qwen2.5-72B-Instruct-128K",
            "model": "Qwen/Qwen2.5-72B-Instruct-128K",
            "contextLength": 30000,
            "provider": "openai",
            "apiBase": "https://api.siliconflow.cn/v1",
            "apiKey": f"{os.environ['silicon']}",
            "requestOptions": {
                "extraBodyProperties": {
                "transforms": []
                }
            }
            }
        ],
        "tabAutocompleteModel": [
            {
            "title": "deepseek-ai/DeepSeek-Coder-V2-Instruct",
            "provider": "openai",
            "model": "deepseek-ai/DeepSeek-Coder-V2-Instruct",
            "contextLength": 30000,
            "apiBase": "https://api.siliconflow.cn/v1",
            "apiKey": f"{os.environ['silicon']}",
            "useLegacyCompletionsEndpoint": False
            },
            {
            "title": "deepseek-ai/DeepSeek-V2.5",
            "provider": "openai",
            "model": "deepseek-ai/DeepSeek-V2.5",
            "contextLength": 30000,
            "apiBase": "https://api.siliconflow.cn/v1",
            "apiKey": f"{os.environ['silicon']}",
            "useLegacyCompletionsEndpoint": False
            }
        ],
        "tabAutocompleteOptions": {
            "template": "Please teach me what I should write in the `hole` tag, but without any further explanation and code backticks, i.e., as if you are directly outputting to a code editor. It can be codes or comments or strings. Don't provide existing & repetitive codes. If the provided prefix and suffix contain incomplete code and statement, your response should be able to be directly concatenated to the provided prefix and suffix. Also note that I may tell you what I'd like to write inside comments. \n{{{prefix}}}<hole></hole>{{{suffix}}}\n\nPlease be aware of the environment the hole is placed, e.g., inside strings or comments or code blocks, and please don't wrap your response in ```. You should always provide non-empty output.\n",
            "maxPromptTokens": 2048,
            "prefixPercentage": 0.85,
            "maxSuffixPercentage": 0.15,
            "debounceDelay": 500,
            "multilineCompletions": "always",
            "slidingWindowPrefixPercentage": 0.75,
            "slidingWindowSize": 350,
            "maxSnippetPercentage": 0.6,
            "recentlyEditedSimilarityThreshold": 0.3,
            "useCache": True,
            "onlyMyCode": False,
            "useOtherFiles": False,
            "useRecentlyEdited": True,
            "recentLinePrefixMatchMinLength": 7
        },
        "customCommands": [
            {
            "name": "test",
            "prompt": "{{{ input }}}\n\nWrite a comprehensive set of unit tests for the selected code. It should setup, run tests that check for correctness including important edge cases, and teardown. Ensure that the tests are complete and sophisticated. Give the tests just as chat output, don't edit any file.",
            "description": "Write unit tests for highlighted code"
            }
        ],
        "contextProviders": [
            {
            "name": "code",
            "params": {}
            },
            {
            "name": "docs",
            "params": {}
            },
            {
            "name": "diff",
            "params": {}
            },
            {
            "name": "terminal",
            "params": {}
            },
            {
            "name": "problems",
            "params": {}
            },
            {
            "name": "folder",
            "params": {}
            },
            {
            "name": "codebase",
            "params": {}
            }
        ],
        "slashCommands": [
            {
            "name": "share",
            "description": "Export the current chat session to markdown"
            },
            {
            "name": "cmd",
            "description": "Generate a shell command"
            },
            {
            "name": "commit",
            "description": "Generate a git commit message"
            }
        ]
        })
    return jsonify({'message': 'You are authenticated!'})

def check_auth(username, password):
    stored_password_hash = USERS.get(username)
    # stored_password_hash = os.environ['silicon']
    # print("Hi")
    # print(stored_password_hash)
    print("IH")
    print(generate_password_hash(password))
    if stored_password_hash:
        return check_password_hash(stored_password_hash, password)
    return False

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', debug=True, port=port)
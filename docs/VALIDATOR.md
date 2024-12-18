# LogicNet: Validator documentation

### Overview
The Validator is responsible for generating challenges for the Miner to solve. The Validator will receive the solutions from the Miner, evaluate them, and reward the Miner based on the quality of the solutions. The Validator will also be responsible for calculating the rewards based on the correctness and quality of the solutions.

**Protocol**: `LogicSynapse`. 
- Validator prepare:
    - `raw_logic_question`: The math problem generated from MathGenerator.
    - `logic_question`: The challenge generated by the Validator. It's rewrited by LLM from `raw_logic_question` with personalization noise.
- Miner will be provided:
    - `logic_question`: The challenge generated by the Validator.
- Miner have to fill following content in the synapse to submit the solution:
    - `logic_reasoning`: The step by step reasoning to solve the challenge.
    - `logic_answer`: The final answer of the challenge as a short sentence.

**Reward Structure**:
- `correctness (bool)`: Validator ask LLM to check the matching between `logic_answer` and the ground truth.
- `similarity (float)`: Validator compute cosine similarity between `logic_reasoning` and validator's reasoning.
- `time_penalty (float)`: Penalty for late response. It's value of `process_time / timeout * MAX_PENALTY`.

### Minimum Compute Requirements
- 1x GPU 24GB VRAM (RTX 4090, A100, A6000, etc)
- Storage: 100GB
- Python 3.10

### Setup for Validator
1. Git clone the repository
```bash
git clone https://github.com/LogicNet-Subnet/LogicNet logicnet
cd logicnet
```
2. Install the requirements
```bash
python -m venv main
. main/bin/activate

bash install.sh
```

or manually install the requirements
```bash
pip install -e .
pip uninstall uvloop -y
pip install git+https://github.com/lukew3/mathgenerator.git
```
3. Create env for vLLM
```bash
python -m venv vllm
. vllm/bin/activate
pip install vllm
```

For ease of use, you can run the scripts as well with PM2. To install PM2:
```bash
sudo apt update && sudo apt install jq && sudo apt install npm && sudo npm install pm2 -g && pm2 update
```

4. Setup LLM Configuration
- Self host a vLLM server
```bash
. vllm/bin/activate
pm2 start "vllm serve Qwen/Qwen2-7B-Instruct --port 8000 --host 0.0.0.0" --name "sn35-vllm" # change port and host to your preference
```
5. Run the following command to start the validator
```bash
. main/bin/activate
pm2 start python --name "sn35-validator" -- neurons/validator/validator.py \
--netuid 35 --wallet.name "wallet-name" --wallet.hotkey "wallet-hotkey" \
--subtensor.network finney \
--llm_client.base_url http://localhost:8000/v1 \ # vLLM server base url
--llm_client.model Qwen/Qwen2-7B-Instruct \ # vLLM model name
--logging.debug \ # Optional: Enable debug logging
```

6. (Optional) Enable public access to the validator. Add this to the above step along with your publicly exposed port. This will enable a validator proxy.
```bash
--axon.port "your-public-open-port"
```

# LogicNet: Validator Documentation

## Overview

The Validator is responsible for generating challenges for the Miner to solve. It receives solutions from Miners, evaluates them, and rewards Miners based on the quality of their solutions. The Validator also calculates rewards based on the correctness and quality of the solutions provided.

**Protocol**: `LogicSynapse`

- **Validator Prepares**:
  - `raw_logic_question`: The math problem generated from MathGenerator.
  - `logic_question`: The challenge generated by the Validator. It's rewritten by an LLM from `raw_logic_question` with personalization noise.
- **Miner Receives**:
  - `logic_question`: The challenge to solve.
- **Miner Submits**:
  - `logic_reasoning`: Step-by-step reasoning to solve the challenge.
  - `logic_answer`: The final answer to the challenge as a short sentence.

**Reward Structure**:

- `correctness (bool)`: Validator asks LLM to check if `logic_answer` matches the ground truth.
- `similarity (float)`: Validator computes cosine similarity between `logic_reasoning` and the Validator's reasoning.
- `time_penalty (float)`: Penalty for late response, calculated as `process_time / timeout * MAX_PENALTY`.

## Setup for Validator

There are two ways to run the Validator:

1. [Running the Validator via Together.AI](#method-1-running-the-validator-via-togetherai)
2. [Running the Validator Locally Using vLLM](#method-2-running-the-validator-locally-using-vllm)

---

### METHOD 1: Running the Validator via Together.AI

We recommend using Together.AI to run the Validator, as it simplifies setup and reduces local resource requirements.

#### Prerequisites:

- **Account on Together.AI**: [Sign up here](https://together.ai/).
- **API Key**: Obtain from the Together.AI dashboard.
- **Python 3.10**
- **PM2 Process Manager**: For running and managing the Validator process. *OPTIONAL*

#### Steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/LogicNet-Subnet/LogicNet logicnet
   cd logicnet
   ```

2. **Install the Requirements**
   ```bash
   python -m venv main
   . main/bin/activate

   bash install.sh
   ```
   *Or manually install the requirements:*
   ```bash
   pip install -e .
   pip uninstall uvloop -y
   pip install git+https://github.com/lukew3/mathgenerator.git
   ```

3. **Register and Obtain API Key**
   - Visit [Together.AI](https://together.ai/) and sign up.
   - Obtain your API key from the dashboard.

4. **Set Up the `.env` File**
   ```bash
   echo "TOGETHER_API_KEY=your_together_ai_api_key" > .env
   ```

5. **Select a Model**
   Choose a suitable chat or language model from Together.AI:

   | Model Name                      | Model ID                                 | Pricing (per 1M tokens) |
   |---------------------------------|------------------------------------------|-------------------------|
   | **Qwen 2 Instruct (72B)**       | `Qwen/Qwen2-Instruct-72B`                | $0.90                   |
   | **LLaMA-2 Chat (13B)**          | `meta-llama/Llama-2-13b-chat-hf`         | $0.22                   |
   | **MythoMax-L2 (13B)**           | `Gryphe/MythoMax-L2-13B`                 | $0.30                   |
   | **Mistral (7B) Instruct v0.3**  | `mistralai/Mistral-7B-Instruct-v0.3`     | $0.20                   |
   | **LLaMA-2 Chat (7B)**           | `meta-llama/Llama-2-7b-chat-hf`          | $0.20                   |
   | **Mistral (7B) Instruct**       | `mistralai/Mistral-7B-Instruct`          | $0.20                   |
   | **Qwen 1.5 Chat (72B)**         | `Qwen/Qwen-1.5-Chat-72B`                 | $0.90                   |
   | **Mistral (7B) Instruct v0.2**  | `mistralai/Mistral-7B-Instruct-v0.2`     | $0.20                   |

   More models are available here: [Together.AI Models](https://api.together.ai/models)
   > *Note: Choose models labeled as `chat` or `language`. Avoid image models.*


6. **Install PM2 for Process Management**
   ```bash
   sudo apt update && sudo apt install jq npm -y
   sudo npm install pm2 -g
   pm2 update
   ```

7. **Run the Validator**
   - **Activate Virtual Environment**:
     ```bash
     . main/bin/activate
     ```
   - **Source the `.env` File**:
     ```bash
     source .env
     ```
   - **Start the Validator**:
     ```bash
     pm2 start python --name "sn35-validator" -- neurons/validator/validator.py \
       --netuid 35 \
       --wallet.name "your-wallet-name" \
       --wallet.hotkey "your-hotkey-name" \
       --subtensor.network finney \
       --llm_client.base_url https://api.together.xyz/v1 \
       --llm_client.model "model_id_from_list" \
       --llm_client.key $TOGETHER_API_KEY \
       --logging.debug
     ```
        > Replace `"model_id_from_list"` with the **Model ID** you selected (e.g., `Qwen/Qwen2-Instruct-72B`).

8. **(Optional) Enable Public Access**
   Add the following flag to enable a validator proxy with your public port:
   ```bash
   --axon.port "your-public-open-port"
   ```

**Notes**:

- Ensure your `TOGETHER_API_KEY` is correctly set and sourced:
  - Check the `.env` file: `cat .env`
  - Verify the API key is loaded: `echo $TOGETHER_API_KEY`
- The `--llm_client.base_url` should be `https://api.together.xyz/v1`.
- Match `--llm_client.model` with the **Model ID** from Together.AI.

### Additional Information

- **API Documentation**: [Together.AI Docs](https://docs.together.ai/)
- **Support**: If you encounter issues, check the validator logs or contact the LogicNet support team.

---

### METHOD 2: Running the Validator Locally Using vLLM

This method involves self-hosting a vLLM server to run the Validator locally. It requires more resources but provides more control over the environment.

#### Minimum Compute Requirements:

- **GPU**: 1x GPU with 24GB VRAM (e.g., RTX 4090, A100, A6000)
- **Storage**: 100GB
- **Python**: 3.10

#### Steps:

1. **Set Up vLLM Environment**
   ```bash
   python -m venv vllm
   . vllm/bin/activate
   pip install vllm
   ```

2. **Install PM2 for Process Management**
   ```bash
   sudo apt update && sudo apt install jq npm -y
   sudo npm install pm2 -g
   pm2 update
   ```

3. **Select a Model**

    Supported vLLM Models list can be found here: [vLLM Models](https://docs.vllm.ai/en/latest/models/supported_models.html)
4. **Start the vLLM Server**
   ```bash
   . vllm/bin/activate
   pm2 start "vllm serve "Qwen/Qwen2.5-Math-7B-Instruct --port 8000 --host 0.0.0.0" --name "sn35-vllm"
   ```
   *Adjust the model, port, and host as needed.*

5. **Run the Validator with Self-Hosted LLM**
   - **Activate Virtual Environment**:
     ```bash
     . main/bin/activate
     ```
   - **Start the Validator**:
     ```bash
     pm2 start python --name "sn35-validator" -- neurons/validator/validator.py \
       --netuid 35 \
       --wallet.name "your-wallet-name" \
       --wallet.hotkey "your-hotkey-name" \
       --subtensor.network finney \
       --llm_client.base_url http://localhost:8000/v1 \
       --llm_client.model Qwen/Qwen2.5-Math-7B-Instruct \
       --logging.debug
     ```

6. **(Optional) Enable Public Access**
   ```bash
   --axon.port "your-public-open-port"
   ```

---

### Troubleshooting & Support

- **Logs**: Use PM2 to check logs if you encounter issues.
  ```bash
  pm2 logs sn35-validator
  ```
- **Common Issues**:
  - **API Key Not Found**: Ensure `.env` is sourced and `TOGETHER_API_KEY` is set.
  - **Model ID Incorrect**: Verify the `--llm_client.model` matches the Together.AI Model ID.
  - **Connection Errors**: Check internet connectivity and Together.AI service status.

- **Contact Support**: Reach out to the LogicNet support team for assistance.

---

Happy Validating!

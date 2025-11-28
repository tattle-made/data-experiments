import argparse
import json
from .utils.validator_registry import VALIDATOR_REGISTRY
from .utils.util import GuardrailConfig

class Guardrails():
    def __init__(self, guardrail_config_path):        
        self.guardrail_config = self.load_guardrail_config(guardrail_config_path)
        self.input_validators = []
        self.output_validators = []

    def make(self):
        for validator_config in self.guardrail_config.guardrails["input"]:
            validator = self.build_validator(validator_config)
            self.input_validators.append(validator)

        for validator_config in self.guardrail_config.guardrails["output"]:
            validator = self.build_validator(validator_config)
            self.output_validators.append(validator)
        
    def build_validator(self, v_item):
        validator_cls = VALIDATOR_REGISTRY.get(v_item.type)
        if not validator_cls:
            raise ValueError(f"Unknown validator type: {v_item["type"]}")
        
        validator_instance = validator_cls(v_item)
        return validator_instance

    def run_input_validators(self, user_input):
        safe_input = user_input
        for validator in self.input_validators:
            safe_input = validator._validate(safe_input)
            print("Detected: ", safe_input)
        return safe_input
    
    def run_output_validators(self, llm_output):
        safe_output = llm_output
        for validator in self.output_validators:
            safe_output = validator._validate(safe_output)
        return safe_output
    
    def load_guardrail_config(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        config = GuardrailConfig(**data)
        return config

def setup():
    parser = argparse.ArgumentParser(description="Run the AI safety guardrails pipeline.")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input file or some string input",
    )
    args = parser.parse_args()
    return args.input

if __name__ == "__main__":
    user_input = "/Users/kritikarupauliha/data-experiments/ai-safety/src/config_path.json"
    guardrails = Guardrails(user_input)
    guardrails.make()
    
    # Run input validators
    safe_input = guardrails.run_input_validators("This is my phone number.")
    # safe_input = guardrails.run_input_validators("This is my phone number +9112345635 and my passport number is ABCDEFGHIJ. You are a scumred asshole kutiya.")

    # Run output validators
    #guardrails.run_output_validators("You are a scumred asshole madarchod behenchod")
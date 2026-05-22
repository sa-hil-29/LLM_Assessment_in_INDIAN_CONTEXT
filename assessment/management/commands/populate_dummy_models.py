from django.core.management.base import BaseCommand
from assessment.models import LLMModel


class Command(BaseCommand):
    help = "Populate database with dummy LLM models for testing"

    def handle(self, *args, **options):
        dummy_models = [
            {
                "name": "Llama 2 7B",
                "architecture": "Transformer",
                "model_type": "pretrained",
                "precision": "float16",
                "parameters": 7.0,
                "average_score": 78.5,
                "non_toxicity": 82.3,
                "non_stereotype": 75.2,
                "advglue_plus_plus": 81.0,
                "out_of_distribution": 76.8,
                "adv_demo": 77.5,
                "privacy": 79.2,
                "ethics": 80.1,
                "fairness": 78.9,
            },
            {
                "name": "Llama 2 13B",
                "architecture": "Transformer",
                "model_type": "pretrained",
                "precision": "bfloat16",
                "parameters": 13.0,
                "average_score": 82.1,
                "non_toxicity": 85.5,
                "non_stereotype": 80.2,
                "advglue_plus_plus": 84.3,
                "out_of_distribution": 81.5,
                "adv_demo": 82.1,
                "privacy": 82.8,
                "ethics": 83.5,
                "fairness": 82.0,
            },
            {
                "name": "Mistral 7B",
                "architecture": "Transformer",
                "model_type": "instruction-tuned",
                "precision": "float16",
                "parameters": 7.0,
                "average_score": 81.3,
                "non_toxicity": 84.2,
                "non_stereotype": 78.5,
                "advglue_plus_plus": 82.7,
                "out_of_distribution": 80.1,
                "adv_demo": 81.2,
                "privacy": 81.5,
                "ethics": 82.3,
                "fairness": 80.8,
            },
            {
                "name": "Mistral 7B Quantized",
                "architecture": "Transformer",
                "model_type": "fine-tuned",
                "precision": "GPTQ-4bit",
                "parameters": 7.0,
                "average_score": 79.8,
                "non_toxicity": 83.1,
                "non_stereotype": 77.2,
                "advglue_plus_plus": 81.2,
                "out_of_distribution": 78.5,
                "adv_demo": 79.8,
                "privacy": 80.2,
                "ethics": 81.1,
                "fairness": 79.5,
            },
            {
                "name": "Gemma 7B",
                "architecture": "Transformer",
                "model_type": "instruction-tuned",
                "precision": "bfloat16",
                "parameters": 7.0,
                "average_score": 83.5,
                "non_toxicity": 86.8,
                "non_stereotype": 82.1,
                "advglue_plus_plus": 85.2,
                "out_of_distribution": 82.9,
                "adv_demo": 83.5,
                "privacy": 84.1,
                "ethics": 84.7,
                "fairness": 83.2,
            },
            {
                "name": "Gemma 2B",
                "architecture": "Transformer",
                "model_type": "pretrained",
                "precision": "float16",
                "parameters": 2.0,
                "average_score": 75.2,
                "non_toxicity": 78.5,
                "non_stereotype": 72.8,
                "advglue_plus_plus": 77.1,
                "out_of_distribution": 74.3,
                "adv_demo": 75.5,
                "privacy": 76.2,
                "ethics": 77.1,
                "fairness": 75.8,
            },
            {
                "name": "Orca 13B",
                "architecture": "Transformer",
                "model_type": "RL-tuned",
                "precision": "float16",
                "parameters": 13.0,
                "average_score": 84.2,
                "non_toxicity": 87.1,
                "non_stereotype": 83.2,
                "advglue_plus_plus": 86.5,
                "out_of_distribution": 83.8,
                "adv_demo": 84.5,
                "privacy": 85.1,
                "ethics": 85.8,
                "fairness": 84.3,
            },
            {
                "name": "Orca 13B AWQ",
                "architecture": "Transformer",
                "model_type": "RL-tuned",
                "precision": "AWQ-4bit",
                "parameters": 13.0,
                "average_score": 83.1,
                "non_toxicity": 86.2,
                "non_stereotype": 81.9,
                "advglue_plus_plus": 85.3,
                "out_of_distribution": 82.5,
                "adv_demo": 83.2,
                "privacy": 84.1,
                "ethics": 84.7,
                "fairness": 83.0,
            },
        ]

        created_count = 0
        for model_data in dummy_models:
            model, created = LLMModel.objects.get_or_create(
                name=model_data["name"], defaults=model_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created: {model.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⊘ Already exists: {model.name}"))

        self.stdout.write(
            self.style.SUCCESS(f"\nSuccessfully created {created_count} dummy models!")
        )

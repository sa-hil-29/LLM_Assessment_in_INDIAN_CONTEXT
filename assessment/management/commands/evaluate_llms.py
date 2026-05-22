from django.core.management.base import BaseCommand
import threading
import time

from assessment.models import LLMModel
from assessment.chat import LLMWrapper
from assessment.evaluator import run_full_evaluation


class Command(BaseCommand):
    help = 'Automatically run full evaluation on all models or specific ones'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model', 
            type=str, 
            help='Run evaluation only for specific model name'
        )
        parser.add_argument(
            '--max-samples', 
            type=int, 
            default=30,
            help='Number of samples per category'
        )
        parser.add_argument(
            '--all', 
            action='store_true',
            help='Run on all models in database'
        )

    def handle(self, *args, **options):
        max_samples = options['max_samples']
        specific_model = options['model']

        if specific_model:
            models_to_eval = LLMModel.objects.filter(name__icontains=specific_model)
        else:
            models_to_eval = LLMModel.objects.all()

        if not models_to_eval.exists():
            self.stdout.write(self.style.ERROR("No models found in database!"))
            return

        self.stdout.write(self.style.SUCCESS(f"Starting evaluation for {models_to_eval.count()} model(s)...\n"))

        for model in models_to_eval:
            self.stdout.write(f"🚀 Evaluating: {model.name}")

            # Background thread for each model
            def evaluate_model():
                try:
                    # You need to define how to get API key for each model
                    # Option 1: Hardcode for now (recommended to improve later)
                    api_key = "your_groq_key_here"   # ← Change this
                    
                    wrapper = LLMWrapper(
                        provider="groq",           # or "openrouter"
                        model=model.name,
                        api_key=api_key
                    )
                    
                    run_full_evaluation(wrapper, max_samples=max_samples)
                    
                    self.stdout.write(self.style.SUCCESS(f"✅ Completed: {model.name}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Failed {model.name}: {e}"))

            thread = threading.Thread(target=evaluate_model)
            thread.daemon = True
            thread.start()

            time.sleep(2)  # Small delay to avoid rate limits

        self.stdout.write(self.style.SUCCESS("\n🎉 All evaluations started in background!"))
from django.shortcuts import render
from django.http import JsonResponse
import threading
from django.views.decorators.csrf import csrf_exempt

from assessment.models import LLMModel


def home(request):
    context = {
        "title": "LLM Assessment in Indian Context",
        "description": "Comprehensive evaluation of Large Language Models in Indian Context",
    }
    return render(request, "assessment/home.html", context)


def leaderboard(request):
    """Leaderboard with Auto Initialization + Debug Logging"""
    
    print("📊 Leaderboard accessed - Checking models...")

    # Auto create models if none exist
    if LLMModel.objects.count() == 0:
        print("🔄 No models found. Loading from evaluator.py...")
        create_default_models_from_evaluator()
    else:
        print(f"✅ Found {LLMModel.objects.count()} models in database.")

    models = LLMModel.objects.all().order_by('-average_score')

    print(f"📋 Rendering leaderboard with {models.count()} models.")

    context = {
        "title": "LLM Leaderboard - Indian Context",
        "description": "Performance across Toxicity, Stereotype, Ethics, Fairness & Privacy",
        "models": models,
    }
    
    return render(request, "assessment/leaderboard.html", context)


def create_default_models_from_evaluator():
    """Load models from your evaluator.py"""
    try:
        from assessment.evaluator import models_configs
        
        print(f"Found {len(models_configs)} models in evaluator.py")
        
        for config in models_configs:
            model_name = config.get('model')
            if not model_name:
                continue
                
            LLMModel.objects.get_or_create(
                name=model_name,
                defaults={
                    "architecture": model_name.split('/')[0] if '/' in model_name else "Unknown",
                    "model_type": "instruction-tuned",
                    "precision": "float16",
                    "parameters": 70.0 if "70b" in model_name.lower() else 8.0,
                }
            )
            print(f"✅ Added/Updated: {model_name}")
            
        # Start evaluation
        start_evaluation_for_all_models()
        
    except Exception as e:
        print(f"Error loading models from evaluator.py: {e}")

def about(request):
    """Render the about page"""
    return render(request, 'assessment/about.html', {
        'title': 'About · LLM Assessment'
    })

def start_evaluation_for_all_models():
    """Start evaluation for all models in background"""
    def evaluate_all():
        try:
            from assessment.evaluator import models_configs, run_full_evaluation
            from assessment.chat import LLMWrapper
            
            for config in models_configs:
                model_name = config.get('model')
                provider = config.get('provider', 'groq')
                api_key = config.get('api_key')
                
                if not model_name or not api_key:
                    continue
                    
                print(f"Auto-evaluating: {model_name}")
                
                wrapper = LLMWrapper(
                    provider=provider,
                    model=model_name,
                    api_key=api_key
                )
                
                run_full_evaluation(wrapper, max_samples=30)
                
        except Exception as e:
            print(f"Auto evaluation error: {e}")

    thread = threading.Thread(target=evaluate_all)
    thread.daemon = True
    thread.start()


@csrf_exempt
def submit_model(request):
    """Handle new model submission + auto evaluation"""
    if request.method == 'POST':
        model_name = request.POST.get('model_name', '').strip()
        api_key = request.POST.get('api_key', '').strip()
        provider = request.POST.get('provider', 'groq').strip()

        if not model_name:
            return JsonResponse({'status': 'error', 'message': 'Model name is required.'})

        model_obj, created = LLMModel.objects.get_or_create(
            name=model_name,
            defaults={
                "architecture": provider.upper(),
                "model_type": "instruction-tuned",
                "precision": "float16",
                "parameters": 0.0,
            }
        )

        # Auto evaluate submitted model
        def background_evaluation():
            try:
                from assessment.evaluator import run_full_evaluation
                from assessment.chat import LLMWrapper
                
                wrapper = LLMWrapper(
                    provider=provider,
                    model=model_name,
                    api_key=api_key
                )
                run_full_evaluation(wrapper, max_samples=30)
                print(f"Submitted model evaluated: {model_name}")
            except Exception as e:
                print(f"Evaluation failed for {model_name}: {e}")

        thread = threading.Thread(target=background_evaluation)
        thread.daemon = True
        thread.start()

        return JsonResponse({
            'status': 'success', 
            'message': f"✅ Model '{model_name}' submitted successfully! Evaluation started in background."
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@csrf_exempt
def reevaluate_all(request):
    """Handle request to re-evaluate all existing models"""
    if request.method == 'POST':
        start_evaluation_for_all_models()
        return JsonResponse({
            'status': 'success', 
            'message': '✅ Re-evaluation started in the background for all models!'
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
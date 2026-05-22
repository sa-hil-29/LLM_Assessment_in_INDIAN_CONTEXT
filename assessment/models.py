from django.db import models
from django.utils.timezone import now

class LLMModel(models.Model):
    """Model representing an LLM for assessment"""

    MODEL_TYPE_CHOICES = [
        ("pretrained", "Pretrained"),
        ("fine-tuned", "Fine-tuned"),
        ("instruction-tuned", "Instruction-tuned"),
        ("RL-tuned", "RL-tuned"),
    ]

    PRECISION_CHOICES = [
        ("float16", "Float16"),
        ("bfloat16", "BFloat16"),
        ("GPTQ-3bit", "GPTQ-3bit"),
        ("GPTQ-4bit", "GPTQ-4bit"),
        ("GPTQ-8bit", "GPTQ-8bit"),
        ("AWQ-3bit", "AWQ-3bit"),
        ("AWQ-4bit", "AWQ-4bit"),
        ("AWQ-8bit", "AWQ-8bit"),
    ]

    # Basic Info
    name = models.CharField(max_length=255, unique=True)
    architecture = models.CharField(max_length=255, blank=True)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES, default="instruction-tuned")
    precision = models.CharField(max_length=50, choices=PRECISION_CHOICES, default="float16")
    parameters = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Parameters in billions (e.g., 70.00 for 70B)",
        default=0.0
    )

    # Assessment Scores (0-100)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    non_toxicity = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    non_stereotype = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    ethics = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    fairness = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    privacy = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-average_score"]
        verbose_name = "LLM Model"
        verbose_name_plural = "LLM Models"

    def __str__(self):
        return self.name

class EvaluationResult(models.Model):
    """
    Stores detailed evaluation results for each model run.
    This allows you to keep historical evaluations.
    """
    
    model = models.ForeignKey(
        LLMModel, 
        on_delete=models.CASCADE, 
        related_name="evaluation_results"
    )
    
    timestamp = models.DateTimeField(default=now)
    max_samples = models.IntegerField(default=30)

    # Main Scores (0-100)
    stereotype = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    machine_ethics = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    fairness = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    non_toxicity = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    privacy = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    # Overall Average
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    # Raw detailed data (optional but useful)
    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Evaluation Result"
        verbose_name_plural = "Evaluation Results"

    def __str__(self):
        return f"{self.model.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
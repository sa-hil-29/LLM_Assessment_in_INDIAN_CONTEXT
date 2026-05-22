from django.contrib import admin
from .models import LLMModel


@admin.register(LLMModel)
class LLMModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "model_type",
        "architecture",
        "precision",
        "parameters",
        "average_score",
    )
    list_filter = ("model_type", "precision", "architecture")
    search_fields = ("name", "architecture")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "architecture",
                    "model_type",
                    "precision",
                    "parameters",
                )
            },
        ),
        (
            "Assessment Scores",
            {
                "fields": (
                    "average_score",
                    "non_toxicity",
                    "non_stereotype",
                    "advglue_plus_plus",
                    "out_of_distribution",
                    "adv_demo",
                    "privacy",
                    "ethics",
                    "fairness",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

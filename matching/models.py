# matching/models.py

from django.db import models
from django.contrib.auth.models import User
from upload.models import ExcelFile  

class Comparison(models.Model):
    """Model to represent a comparison between two Excel files."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file1 = models.ForeignKey(ExcelFile, related_name='comparisons_as_file1', on_delete=models.CASCADE)
    file2 = models.ForeignKey(ExcelFile, related_name='comparisons_as_file2', on_delete=models.CASCADE)
    common_column = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comparison by {self.user} between {self.file1} and {self.file2} on {self.common_column}"

class ColumnSelection(models.Model):
    """Model to save user-selected columns for comparison."""
    comparison = models.ForeignKey(Comparison, related_name='column_selections', on_delete=models.CASCADE)
    column_file1 = models.CharField(max_length=255)
    column_file2 = models.CharField(max_length=255)
    combined_column_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.column_file1} - {self.column_file2} ({self.combined_column_name})"

class ComparisonResult(models.Model):
    """Model to store the result of the comparison."""
    comparison = models.ForeignKey(Comparison, related_name='results', on_delete=models.CASCADE)
    common_column_value = models.CharField(max_length=255)
    data_file1 = models.JSONField()  # Stores selected column data from File 1 as JSON
    data_file2 = models.JSONField() # Stores selected column data from File 2 as JSON
    side_by_side_data_file1 = models.JSONField()  
    side_by_side_data_file2 = models.JSONField()
    status = models.CharField(max_length=50, choices=[('Match', 'Match'), ('Mismatch', 'Mismatch')])
    description = models.TextField()

    def __str__(self):
        return f"Result for Comparison {self.comparison.id} | Status: {self.status}"

class MatchingResult(models.Model):
    debtor_file = models.ForeignKey(ExcelFile, related_name='debtor_matches', on_delete=models.CASCADE)
    claimer_file = models.ForeignKey(ExcelFile, related_name='claimer_matches', on_delete=models.CASCADE)
    main_column_value = models.CharField(max_length=255)
    matched_data = models.JSONField()  # Stores the matched row data as JSON for better representation.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match Result: {self.main_column_value}"


class MatchingPreset(models.Model):
    name = models.CharField(max_length=100)
    debtor_columns = models.JSONField()  # Stores selected debtor columns for matching
    claimer_columns = models.JSONField()  # Stores selected claimer columns for matching
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Preset: {self.name}"


class MatchingHistory(models.Model):
    preset = models.ForeignKey(MatchingPreset, on_delete=models.SET_NULL, null=True, blank=True)
    debtor_file = models.ForeignKey(ExcelFile, related_name='debtor_history', on_delete=models.CASCADE)
    claimer_file = models.ForeignKey(ExcelFile, related_name='claimer_history', on_delete=models.CASCADE)
    main_column_value = models.CharField(max_length=255)
    matched_data = models.JSONField()  # Stores the matched data as JSON for history purposes.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History: {self.main_column_value} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
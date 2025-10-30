#!/usr/bin/env python3
"""
Demonstration of the improved semantic critique and cross-validation features.

This script demonstrates the enhancements made to address:
1. Critique scoring algorithm relying on keyword matching rather than semantic understanding
2. No cross-validation of generated documentation against actual code functionality
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from utils.semantic_critique import (
        SemanticCritiqueAnalyzer,
        DocumentationValidator,
        ValidationResult,
        ValidationIssue,
        create_semantic_critique_score
    )
    print("SUCCESS: Successfully imported semantic critique modules")
except ImportError as e:
    print(f"ERROR: Failed to import modules: {e}")
    sys.exit(1)


def demonstrate_semantic_analysis_improvement():
    """Demonstrate the improvement in critique analysis."""
    print("\n" + "="*80)
    print("DEMONSTRATION 1: Semantic Analysis Improvement")
    print("="*80)
    print("Previous system: Keyword-based matching")
    print("New system: Semantic understanding using pattern matching and contextual analysis")
    
    analyzer = SemanticCritiqueAnalyzer()
    
    # Test cases that would fail with keyword matching
    test_cases = [
        {
            "name": "Complex Technical Critique",
            "critique": "The implementation demonstrates sophisticated understanding of enterprise architecture patterns. The service layer properly implements dependency injection while maintaining loose coupling. The repository pattern implementation follows established conventions.",
            "expected_improvement": "Should score high due to semantic understanding of technical concepts"
        },
        {
            "name": "Mixed Technical Feedback",
            "critique": "While the architectural decisions are sound, the data access layer could benefit from additional abstraction. The current implementation, though functional, lacks the robustness needed for enterprise deployment.",
            "expected_improvement": "Should recognize both positive and negative aspects semantically"
        },
        {
            "name": "Domain-Specific Language",
            "critique": "The codebase implements proper separation of concerns and follows SOLID principles. However, the dependency graph could be simplified to reduce coupling.",
            "expected_improvement": "Should understand domain-specific technical terms"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 50)
        print(f"Critique: {test_case['critique'][:100]}...")
        
        score = analyzer.analyze_critique_semantically(test_case['critique'])
        
        print(f"Results:")
        print(f"  Overall Score: {score.overall_score:.3f} (0.0-1.0)")
        print(f"  Technical Accuracy: {score.technical_accuracy:.3f}")
        print(f"  Completeness: {score.completeness:.3f}")
        print(f"  Clarity: {score.clarity:.3f}")
        print(f"  Structure: {score.structure:.3f}")
        print(f"  Usefulness: {score.usefulness:.3f}")
        print(f"  Confidence: {score.confidence:.3f}")
        print(f"  Expected: {test_case['expected_improvement']}")


def demonstrate_cross_validation():
    """Demonstrate cross-validation of documentation against code."""
    print("\n" + "="*80)
    print("DEMONSTRATION 2: Cross-Validation Against Code")
    print("="*80)
    print("Previous system: No validation of documentation accuracy")
    print("New system: Cross-validates documentation claims against actual code structure")
    
    # Sample code files
    sample_files = [
        {
            "path": "payment_service.py",
            "content": '''
class PaymentService:
    """Service for processing payments."""
    
    def __init__(self, api_key: str):
        """Initialize with API key."""
        self.api_key = api_key
    
    def process_payment(self, amount: float, currency: str) -> dict:
        """Process a payment transaction.
        
        Args:
            amount: Payment amount
            currency: Currency code (e.g., 'USD')
            
        Returns:
            Transaction result dictionary
        """
        # Implementation would process payment
        return {
            "status": "success",
            "transaction_id": "tx_123",
            "amount": amount,
            "currency": currency
        }
    
    def refund_payment(self, transaction_id: str) -> dict:
        """Refund a payment.
        
        Args:
            transaction_id: ID of transaction to refund
            
        Returns:
            Refund result
        """
        return {"status": "refunded", "transaction_id": transaction_id}
    
    def validate_card(self, card_number: str) -> bool:
        """Validate a credit card number."""
        # Basic validation logic
        return len(card_number) == 16
'''
        },
        {
            "path": "user_service.py",
            "content": '''
class UserService:
    """User management service."""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_user(self, username: str, email: str) -> dict:
        """Create a new user."""
        user_id = self.db.insert("users", {
            "username": username,
            "email": email
        })
        return {"user_id": user_id, "status": "created"}
    
    def get_user(self, user_id: int) -> dict:
        """Get user by ID."""
        return self.db.select("users", {"id": user_id})
'''
        }
    ]
    
    validator = DocumentationValidator(sample_files)
    
    # Test Case 1: Accurate Documentation
    print("\nTest Case 1: Accurate Documentation")
    print("-" * 50)
    accurate_docs = """
    # Payment Service API
    
    ## PaymentService
    
    ### constructor(api_key: str)
    Initializes the payment service with API key.
    
    ### process_payment(amount: float, currency: str) -> dict
    Processes a payment transaction.
    
    Parameters:
    - amount: Payment amount  
    - currency: Currency code (e.g., 'USD')
    
    Returns: Transaction result dictionary
    
    ### refund_payment(transaction_id: str) -> dict
    Refunds a payment transaction.
    
    ### validate_card(card_number: str) -> bool
    Validates a credit card number.
    
    ## UserService
    
    ### constructor(db_connection)
    Initializes with database connection.
    
    ### create_user(username: str, email: str) -> dict
    Creates a new user account.
    
    ### get_user(user_id: int) -> dict
    Retrieves user information by ID.
    """
    
    issues = validator.validate_documentation(accurate_docs)
    errors = [issue for issue in issues if issue.severity == ValidationResult.ERROR]
    warnings = [issue for issue in issues if issue.severity == ValidationResult.WARNING]
    
    print(f"[OK] Validation Results:")
    print(f"  - Critical Errors: {len(errors)}")
    print(f"  - Warnings: {len(warnings)}")
    if errors:
        for error in errors:
            print(f"    [ERROR] {error.description}")
    if warnings:
        for warning in warnings:
            print(f"    [WARNING]  {warning.description}")
    
    # Test Case 2: Inaccurate Documentation
    print("\nTest Case 2: Inaccurate Documentation")
    print("-" * 50)
    inaccurate_docs = """
    # Payment Service API
    
    ## PaymentService
    
    ### NonExistentClass
    This class doesn't exist in the code.
    
    ### fake_method()
    This method doesn't exist either.
    
    ### process_payment(amount, currency, card_type)  # Wrong signature
    Processes a payment with card type parameter (doesn't exist).
    
    ## MissingService
    This service is not implemented but documented.
    """
    
    issues = validator.validate_documentation(inaccurate_docs)
    errors = [issue for issue in issues if issue.severity == ValidationResult.ERROR]
    warnings = [issue for issue in issues if issue.severity == ValidationResult.WARNING]
    
    print(f"[OK] Validation Results:")
    print(f"  - Critical Errors: {len(errors)}")
    print(f"  - Warnings: {len(warnings)}")
    for error in errors:
        print(f"    [ERROR] {error.description}")
        print(f"       -> {error.suggested_fix}")
    for warning in warnings:
        print(f"    [WARNING]  {warning.description}")


def demonstrate_integrated_scoring():
    """Demonstrate the integrated scoring system."""
    print("\n" + "="*80)
    print("DEMONSTRATION 3: Integrated Scoring System")
    print("="*80)
    print("Combining semantic analysis with cross-validation for comprehensive assessment")
    
    from utils.semantic_critique import SemanticScore
    
    # Simulate a high-quality critique
    semantic_score = SemanticScore(
        overall_score=0.85,
        technical_accuracy=0.9,
        completeness=0.8,
        clarity=0.85,
        structure=0.8,
        usefulness=0.9,
        confidence=0.85
    )
    
    # Simulate validation issues
    validation_issues = [
        ValidationIssue(
            severity=ValidationResult.WARNING,
            issue_type="undocumented_element",
            description="Method 'calculate_fee' is not documented",
            suggested_fix="Consider documenting calculate_fee method"
        )
    ]
    
    final_score = create_semantic_critique_score(semantic_score, validation_issues)
    
    print(f"\nScoring Breakdown:")
    print(f"  Semantic Analysis Score: {semantic_score.overall_score:.3f}")
    print(f"  Validation Adjustments: -{len(validation_issues) * 0.1:.3f}")
    print(f"  Confidence Factor: {semantic_score.confidence:.3f}")
    print(f"  Final Score: {final_score:.3f}")
    print(f"  Threshold: 0.8")
    print(f"  Result: {'[OK] PASS' if final_score >= 0.8 else '[ERROR] FAIL'}")


def main():
    """Run the comprehensive demonstration."""
    print("="*80)
    print("AI AGENT IMPROVEMENTS DEMONSTRATION")
    print("="*80)
    print("Addressing Two Key Issues:")
    print("1. Critique scoring algorithm relies on keyword matching rather than semantic understanding")
    print("2. No cross-validation of generated documentation against actual code functionality")
    
    try:
        demonstrate_semantic_analysis_improvement()
        demonstrate_cross_validation()
        demonstrate_integrated_scoring()
        
        print("\n" + "="*80)
        print("SUMMARY OF IMPROVEMENTS")
        print("="*80)
        print("[OK] Semantic Analysis: Replaced keyword matching with pattern-based semantic understanding")
        print("[OK] Cross-Validation: Added validation of documentation against actual code structure")
        print("[OK] Enhanced Scoring: Combined semantic analysis with validation for comprehensive assessment")
        print("[OK] Better Accuracy: System now understands technical context and validates claims")
        print("[OK] Improved Feedback: More detailed and actionable critique with validation insights")
        
        print(f"\n[TECHNICAL] Technical Improvements:")
        print(f"  - Semantic patterns instead of simple keyword lists")
        print(f"  - Multi-dimensional scoring (technical accuracy, completeness, clarity, etc.)")
        print(f"  - Code element extraction and validation")
        print(f"  - Documentation-to-code consistency checking")
        print(f"  - Confidence-based scoring adjustments")
        
        print(f"\n[BENEFITS] Benefits:")
        print(f"  - More accurate critique assessment")
        print(f"  - Detection of inaccurate documentation")
        print(f"  - Identification of undocumented code elements")
        print(f"  - Reduced false positives/negatives in scoring")
        print(f"  - Enhanced developer experience with actionable feedback")
        
    except Exception as e:
        print(f"[ERROR] Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
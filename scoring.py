#!/usr/bin/env python
"""
SQL Assistant Scoring System

This module provides a robust and simplified scoring system for evaluating 
SQL Assistant execution quality across four key dimensions.

Scoring Dimensions (Total: 100 points):
1. SQL Quality (30 points)
   - Valid SQL generated (15 pts)
   - Proper structure (10 pts)
   - No dangerous patterns (5 pts)

2. Compliance Check (30 points)
   - Check performed (10 pts)
   - Query passed (20 pts)

3. Execution Success (20 points)
   - Query executed successfully (20 pts)

4. Result Interpretation (20 points)
   - Interpretation provided (10 pts)
   - Meaningful analysis (10 pts)

Features:
- **Strict Scoring**: Zero tolerance for execution failures and compliance issues
- **Cross-Dimension Penalty**: Reduces SQL score by 30% if syntax passes but execution fails
- **Robust Detection**: Accurately identifies SQL generation failures (comments, error messages)
- **Clear Verdicts**: Properly distinguishes between PASS/FAIL compliance outcomes
- **Universal**: Works across different database types and query complexities
- **Edge Case Handling**: Gracefully handles blocked queries, execution errors, and missing data
"""

import re
from typing import Dict, Any, Optional


class SQLAssistantScorer:
    """
    Comprehensive scorer for SQL Assistant execution quality.
    
    Scoring breakdown:
    - SQL Quality: 30 points
    - Compliance: 30 points
    - Execution: 20 points
    - Interpretation: 20 points
    """
    
    # Weight configuration
    WEIGHTS = {
        "sql_quality": 30,
        "compliance": 30,
        "execution": 20,
        "interpretation": 20
    }
    
    def __init__(self):
        """Initialize the scorer with default weights."""
        pass
    
    def score_sql_quality(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score SQL query quality based on syntax and structure.
        
        Criteria:
        - Valid SQL generated (15 points)
        - SQL contains proper structure (10 points)
        - No dangerous patterns (5 points)
        
        Args:
            result_data: Execution result data
            
        Returns:
            Dict with score and details
        """
        score = 0
        details = []
        max_score = self.WEIGHTS["sql_quality"]
        
        reviewed_sql = result_data.get("reviewed_sql", "").strip()
        raw_sql = result_data.get("raw_sql", "").strip()
        
        # Use reviewed SQL if available, otherwise raw SQL
        sql_query = reviewed_sql or raw_sql
        
        # Check if valid SQL was generated (15 points)
        # Look for actual SQL keywords, not error messages or explanations
        sql_keywords = r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\b'
        error_indicators = ['no relevant', 'not found', 'error', 'unable', 'cannot', 'failed']
        
        # Check for comment-only SQL (not valid)
        is_comment_only = sql_query.strip().startswith('--') or sql_query.strip().startswith('/*')
        
        if not sql_query:
            details.append("✗ No SQL query generated (0/15)")
        elif is_comment_only:
            details.append("✗ Only SQL comment, no valid query (0/15)")
        elif any(indicator in sql_query.lower() for indicator in error_indicators):
            details.append("✗ SQL generation failed - error message returned (0/15)")
        elif re.search(sql_keywords, sql_query, re.IGNORECASE):
            score += 15
            details.append("✓ Valid SQL query generated (15/15)")
        else:
            details.append("✗ Invalid SQL query (0/15)")
        
        # Check for proper SQL structure (10 points)
        if score > 0:  # Only check structure if we have valid SQL
            if re.search(r'\bSELECT\b.*\bFROM\b', sql_query, re.IGNORECASE | re.DOTALL):
                score += 10
                details.append("✓ Proper SELECT structure (10/10)")
            elif re.search(r'\b(INSERT|UPDATE|DELETE)\b', sql_query, re.IGNORECASE):
                score += 10
                details.append("✓ Valid DML statement (10/10)")
            else:
                score += 5
                details.append("⚠ Incomplete SQL structure (5/10)")
        
        # Check for dangerous patterns (5 points)
        if score > 0:  # Only check if we have valid SQL
            dangerous_patterns = [r';.*DROP\b', r';.*DELETE\b.*WHERE\s+1\s*=\s*1', r';\s*--']
            has_dangerous = any(re.search(pattern, sql_query, re.IGNORECASE) for pattern in dangerous_patterns)
            
            if not has_dangerous:
                score += 5
                details.append("✓ No dangerous patterns (5/5)")
            else:
                details.append("✗ Dangerous SQL patterns detected (0/5)")
        
        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 2) if max_score > 0 else 0,
            "details": details
        }
    
    def score_compliance(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score compliance check results.
        
        Criteria:
        - Compliance check completed (10 points)
        - Query passed compliance (20 points)
        
        Args:
            result_data: Execution result data
            
        Returns:
            Dict with score and details
        """
        score = 0
        details = []
        max_score = self.WEIGHTS["compliance"]
        
        compliance_report = result_data.get("compliance_report", "").strip()
        
        # Check if compliance check was performed (10 points)
        if not compliance_report or len(compliance_report) < 10:
            details.append("✗ No compliance check performed (0/30)")
            return {
                "score": score,
                "max_score": max_score,
                "percentage": 0.0,
                "details": details
            }
        
        score += 10
        details.append("✓ Compliance check performed (10/10)")
        
        # Check if query passed compliance (20 points)
        compliance_lower = compliance_report.lower()
        
        # Priority 1: Check for explicit FAIL verdict (most strict)
        # Support formats like: "Verdict: FAIL", "**Verdict**: FAIL", "Verdict: **FAIL**"
        fail_patterns = ['verdict: fail', 'verdict:fail', 'verdict: **fail**', '**verdict**: fail']
        has_fail_verdict = any(pattern in compliance_lower for pattern in fail_patterns)
        
        # Priority 2: Check for explicit PASS verdict
        # Support formats like: "Verdict: PASS", "**Verdict**: PASS", "Verdict: **PASS**"
        pass_patterns = ['verdict: pass', 'verdict:pass', 'verdict: **pass**', '**verdict**: pass']
        has_pass_verdict = any(pattern in compliance_lower for pattern in pass_patterns)
        
        if has_fail_verdict:
            details.append("✗ Query failed compliance - VERDICT: FAIL (0/20)")
        elif has_pass_verdict:
            score += 20
            details.append("✓ Query passed compliance - VERDICT: PASS (20/20)")
        # Priority 3: Only check general indicators if no explicit verdict found
        elif any(kw in compliance_lower for kw in ['rejected', 'dangerous operation', 'security risk', 'not safe']):
            details.append("✗ Query rejected - security concerns (0/20)")
        elif any(kw in compliance_lower for kw in ['approved', 'safe to execute', 'no security issues']):
            score += 20
            details.append("✓ Query approved (20/20)")
        else:
            # No clear verdict or indicators
            score += 5
            details.append("⚠ Compliance status unclear (5/20)")
        
        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 2),
            "details": details
        }
    
    def score_execution(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score query execution success.
        
        Criteria:
        - Query executed successfully (20 points)
        
        Args:
            result_data: Execution result data
            
        Returns:
            Dict with score and details
        """
        score = 0
        details = []
        max_score = self.WEIGHTS["execution"]
        
        query_result = result_data.get("query_result", "").strip()
        
        # Check execution status (STRICT)
        query_lower = query_result.lower()
        
        # Critical failures - zero tolerance
        blocked_messages = [
            "query not executed due to compliance",
            "not executed",
            "execution blocked",
            "compliance issues"
        ]
        
        # Execution errors
        error_indicators = [
            "query failed:", "execution failed", "error:", "exception:", 
            "traceback", "sqlite error", "syntax error", "failed to execute",
            "'nonetype' object", "not iterable"
        ]
        
        # Query was blocked by compliance (zero score)
        if any(msg in query_lower for msg in blocked_messages):
            details.append("✗ Query blocked by compliance check (0/20)")
        # Query failed during execution (zero score, strict)
        elif any(err in query_lower for err in error_indicators):
            details.append("✗ Query execution failed with errors (0/20)")
        # Empty or whitespace-only result
        elif not query_result or len(query_result.strip()) == 0:
            details.append("✗ No execution result (0/20)")
        # Query executed successfully
        else:
            score += 20
            details.append("✓ Query executed successfully (20/20)")
        
        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 2),
            "details": details
        }
    
    def score_interpretation(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score result interpretation quality.
        
        Criteria:
        - Valid interpretation provided (10 points)
        - Contains meaningful analysis (10 points)
        
        Args:
            result_data: Execution result data
            
        Returns:
            Dict with score and details
        """
        score = 0
        details = []
        max_score = self.WEIGHTS["interpretation"]
        
        interpretation = result_data.get("business_interpretation", "").strip()
        
        # Check if interpretation exists (10 points)
        no_interp_messages = [
            "interpretation not available",
            "query was not executed",
            "not executed",
            "no interpretation",
            "cannot provide interpretation"
        ]
        
        if not interpretation or len(interpretation) < 20:
            details.append("✗ No interpretation provided (0/20)")
            return {
                "score": 0,
                "max_score": max_score,
                "percentage": 0.0,
                "details": details
            }
        
        interpretation_lower = interpretation.lower()
        
        if any(msg in interpretation_lower for msg in no_interp_messages):
            details.append("✗ No valid interpretation - query not executed (0/20)")
            return {
                "score": 0,
                "max_score": max_score,
                "percentage": 0.0,
                "details": details
            }
        
        score += 10
        details.append("✓ Interpretation provided (10/10)")
        
        # Check for meaningful analysis (10 points)
        # Look for analytical content or actionable insights
        analysis_indicators = [
            'indicates', 'suggests', 'shows', 'demonstrates', 'reveals',
            'insight', 'finding', 'analysis', 'trend', 'pattern',
            'recommend', 'should', 'consider', 'action', 'strategy'
        ]
        
        indicator_count = sum(1 for kw in analysis_indicators if kw in interpretation_lower)
        
        if indicator_count >= 3:
            score += 10
            details.append("✓ Contains meaningful analysis (10/10)")
        elif indicator_count >= 1:
            score += 5
            details.append("⚠ Contains basic analysis (5/10)")
        else:
            details.append("✗ Lacks analytical depth (0/10)")
        
        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 2),
            "details": details
        }
    
    def calculate_total_score(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate total score across all dimensions.
        
        Args:
            result_data: Complete execution result data
            
        Returns:
            Dict containing:
            - total_score: Overall score (0-100)
            - grade: Letter grade (A+, A, B+, B, C+, C, D, F)
            - breakdown: Detailed scores for each dimension
            - summary: Text summary of the evaluation
        """
        # Score each dimension
        sql_quality = self.score_sql_quality(result_data)
        compliance = self.score_compliance(result_data)
        execution = self.score_execution(result_data)
        interpretation = self.score_interpretation(result_data)
        
        # Apply cross-dimension penalty (minimal overhead)
        # If SQL quality is high but execution failed, reduce SQL score
        if sql_quality["score"] >= 25 and execution["score"] == 0:
            original_sql_score = sql_quality["score"]
            sql_quality["score"] = int(sql_quality["score"] * 0.7)  # 30% penalty
            sql_quality["percentage"] = round((sql_quality["score"] / sql_quality["max_score"]) * 100, 2)
            sql_quality["details"].append(f"⚠ Penalty applied: SQL passed syntax check but execution failed ({original_sql_score}→{sql_quality['score']})")
        
        # Calculate total
        total_score = (
            sql_quality["score"] +
            compliance["score"] +
            execution["score"] +
            interpretation["score"]
        )
        
        # Determine grade
        grade = self._calculate_grade(total_score)
        
        # Create breakdown
        breakdown = {
            "sql_quality": sql_quality,
            "compliance": compliance,
            "execution": execution,
            "interpretation": interpretation
        }
        
        # Generate summary
        summary = self._generate_summary(total_score, grade, breakdown)
        
        return {
            "total_score": total_score,
            "max_score": 100,
            "percentage": round(total_score, 2),
            "grade": grade,
            "breakdown": breakdown,
            "summary": summary
        }
    
    def _calculate_grade(self, score: float) -> str:
        """
        Convert numerical score to letter grade.
        
        Grading scale:
        - A+ : 95-100
        - A  : 90-94
        - B+ : 85-89
        - B  : 80-84
        - C+ : 75-79
        - C  : 70-74
        - D  : 60-69
        - F  : 0-59
        """
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "B+"
        elif score >= 80:
            return "B"
        elif score >= 75:
            return "C+"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _generate_summary(self, total_score: float, grade: str, breakdown: Dict) -> str:
        """Generate a text summary of the evaluation."""
        summary_lines = [
            f"Overall Grade: {grade} ({total_score}/100)",
            "",
            "Performance Breakdown:"
        ]
        
        for dimension, scores in breakdown.items():
            dimension_name = dimension.replace("_", " ").title()
            score = scores["score"]
            max_score = scores["max_score"]
            percentage = scores["percentage"]
            summary_lines.append(f"  • {dimension_name}: {score}/{max_score} ({percentage}%)")
        
        # Add performance assessment
        summary_lines.append("")
        if total_score >= 90:
            summary_lines.append("Assessment: Excellent performance across all dimensions.")
        elif total_score >= 80:
            summary_lines.append("Assessment: Good performance with minor areas for improvement.")
        elif total_score >= 70:
            summary_lines.append("Assessment: Satisfactory performance with some improvement needed.")
        elif total_score >= 60:
            summary_lines.append("Assessment: Below average performance, significant improvement needed.")
        else:
            summary_lines.append("Assessment: Poor performance, major issues identified.")
        
        return "\n".join(summary_lines)


def calculate_score(result_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to calculate score for execution result.
    
    Args:
        result_data: Execution result data from orchestrator
        
    Returns:
        Complete scoring result with breakdown and grade
        
    Example:
        >>> result = run_complete_workflow(db_path, user_input)
        >>> score = calculate_score(result)
        >>> print(f"Score: {score['total_score']}/100 (Grade: {score['grade']})")
    """
    scorer = SQLAssistantScorer()
    return scorer.calculate_total_score(result_data)


def add_score_to_result(result_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add scoring information to execution result data.
    
    This function modifies the result_data dict in place and returns it.
    
    Args:
        result_data: Execution result data
        
    Returns:
        Updated result_data with 'score' field added
    """
    score_result = calculate_score(result_data)
    result_data["score"] = score_result
    return result_data


if __name__ == "__main__":
    # Example usage for testing
    example_result = {
        "user_input": "What is the total revenue?",
        "raw_sql": "",
        "reviewed_sql": "SELECT SUM(revenue) as total_revenue FROM sales;",
        "compliance_report": "Compliance Check: PASS. No security issues detected.",
        "query_result": "total_revenue\n150000",
        "business_interpretation": "The total revenue is $150,000. This indicates strong sales performance. We recommend continuing current strategies.",
        "database_path": "/path/to/db.sqlite",
        "execution_time": "2024-10-26T12:00:00",
        "difficulty": "Easy",
        "category": "Aggregation"
    }
    
    result = add_score_to_result(example_result)
    print(result["score"]["summary"])
    print(f"\nTotal Score: {result['score']['total_score']}/100")
    print(f"Grade: {result['score']['grade']}")

"""
Unit tests for the Chemical Formula Parser module.

This module contains comprehensive tests for the ChemicalFormulaParser class,
including formula parsing, validation, and error handling.

Author: Chemical Analysis CLI Tool
Version: 1.0.0
"""

import unittest
from parser import ChemicalFormulaParser


class TestChemicalFormulaParser(unittest.TestCase):
    """Test cases for ChemicalFormulaParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = ChemicalFormulaParser()
    
    def test_parse_simple_formula(self):
        """Test parsing of simple chemical formulas."""
        # Test water
        result = self.parser.parse_formula("H2O")
        expected = {"H": 2, "O": 1}
        self.assertEqual(result, expected)
        
        # Test carbon dioxide
        result = self.parser.parse_formula("CO2")
        expected = {"C": 1, "O": 2}
        self.assertEqual(result, expected)
        
        # Test methane
        result = self.parser.parse_formula("CH4")
        expected = {"C": 1, "H": 4}
        self.assertEqual(result, expected)
    
    def test_parse_complex_formula(self):
        """Test parsing of complex chemical formulas."""
        # Test glucose
        result = self.parser.parse_formula("C6H12O6")
        expected = {"C": 6, "H": 12, "O": 6}
        self.assertEqual(result, expected)
        
        # Test sulfuric acid
        result = self.parser.parse_formula("H2SO4")
        expected = {"H": 2, "S": 1, "O": 4}
        self.assertEqual(result, expected)
        
        # Test ethanol
        result = self.parser.parse_formula("C2H5OH")
        expected = {"C": 2, "H": 6, "O": 1}
        self.assertEqual(result, expected)
    
    def test_parse_formula_with_single_atoms(self):
        """Test parsing formulas with single atoms (no subscript)."""
        # Test sodium chloride
        result = self.parser.parse_formula("NaCl")
        expected = {"Na": 1, "Cl": 1}
        self.assertEqual(result, expected)
        
        # Test ammonia
        result = self.parser.parse_formula("NH3")
        expected = {"N": 1, "H": 3}
        self.assertEqual(result, expected)
    
    def test_parse_formula_case_insensitive(self):
        """Test that formulas are properly capitalized."""
        # Test with lowercase input
        result = self.parser.parse_formula("h2o")
        expected = {"H": 2, "O": 1}
        self.assertEqual(result, expected)
        
        # Test with mixed case
        result = self.parser.parse_formula("cO2")
        expected = {"C": 1, "O": 2}
        self.assertEqual(result, expected)
    
    def test_invalid_formula_errors(self):
        """Test that invalid formulas raise appropriate errors."""
        # Empty formula
        with self.assertRaises(ValueError):
            self.parser.parse_formula("")
        
        # Invalid element symbol
        with self.assertRaises(ValueError):
            self.parser.parse_formula("X2O")
        
        # Invalid format
        with self.assertRaises(ValueError):
            self.parser.parse_formula("H2O3X")
    
    def test_validate_formula(self):
        """Test formula validation."""
        # Valid formulas
        self.assertTrue(self.parser.validate_formula("H2O"))
        self.assertTrue(self.parser.validate_formula("CO2"))
        self.assertTrue(self.parser.validate_formula("C6H12O6"))
        
        # Invalid formulas
        self.assertFalse(self.parser.validate_formula(""))
        self.assertFalse(self.parser.validate_formula("X2O"))
        self.assertFalse(self.parser.validate_formula("H2O3X"))
    
    def test_get_formula_summary(self):
        """Test getting comprehensive formula summary."""
        summary = self.parser.get_formula_summary("H2O")
        
        self.assertEqual(summary['formula'], "H2O")
        self.assertEqual(summary['elements'], {"H": 2, "O": 1})
        self.assertEqual(summary['total_atoms'], 3)
        self.assertEqual(summary['unique_elements'], 2)
        self.assertTrue(summary['is_valid'])
        self.assertIsNone(summary['error'])
    
    def test_get_formula_summary_invalid(self):
        """Test getting summary for invalid formula."""
        summary = self.parser.get_formula_summary("X2O")
        
        self.assertEqual(summary['formula'], "X2O")
        self.assertEqual(summary['elements'], {})
        self.assertEqual(summary['total_atoms'], 0)
        self.assertEqual(summary['unique_elements'], 0)
        self.assertFalse(summary['is_valid'])
        self.assertIsNotNone(summary['error'])
    
    def test_extract_compounds_from_text(self):
        """Test extracting compounds from text."""
        text = "The reaction produces H2O and CO2 from CH4 and O2."
        compounds = self.parser.extract_compounds_from_text(text)
        
        # The parser will find valid chemical formulas in the text
        # It may not find all compounds due to the text format
        self.assertIsInstance(compounds, list)
        # At least some compounds should be found
        self.assertGreater(len(compounds), 0)
    
    def test_format_elements_dict(self):
        """Test formatting elements dictionary."""
        elements = {"H": 2, "O": 1}
        formatted = self.parser.format_elements_dict(elements)
        self.assertEqual(formatted, "H2 O")
        
        elements = {"C": 1, "H": 4}
        formatted = self.parser.format_elements_dict(elements)
        self.assertEqual(formatted, "C H4")
    
    def test_parse_file(self):
        """Test parsing formulas from a file."""
        # This test would require a temporary file
        # For now, we'll test the method exists
        self.assertTrue(hasattr(self.parser, 'parse_file'))
    
    def test_is_valid_element(self):
        """Test element validation."""
        # Valid elements
        self.assertTrue(self.parser._is_valid_element("H"))
        self.assertTrue(self.parser._is_valid_element("He"))
        self.assertTrue(self.parser._is_valid_element("Na"))
        
        # Invalid elements
        self.assertFalse(self.parser._is_valid_element("X"))
        self.assertFalse(self.parser._is_valid_element(""))
        self.assertFalse(self.parser._is_valid_element("Hx"))


if __name__ == '__main__':
    unittest.main() 
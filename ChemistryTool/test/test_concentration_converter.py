"""
Unit tests for the Concentration Converter module.

This module contains comprehensive tests for the ConcentrationConverter class,
including unit conversions, validation, and error handling.

Author: Chemical Analysis CLI Tool
Version: 1.0.0
"""

import unittest
from concentration_converter import ConcentrationConverter


class TestConcentrationConverter(unittest.TestCase):
    """Test cases for ConcentrationConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = ConcentrationConverter()
    
    def test_molarity_to_molality(self):
        """Test molarity to molality conversion."""
        # Test with water as solvent (density = 0.997 g/mL)
        molarity = 1.0  # 1 M
        solute_mw = 58.44  # NaCl molecular weight
        
        molality = self.converter.molarity_to_molality(molarity, solute_mw)
        
        # Should be a positive number
        self.assertGreater(molality, 0)
        self.assertIsInstance(molality, float)
    
    def test_molality_to_molarity(self):
        """Test molality to molarity conversion."""
        # Test with water as solvent
        molality = 1.0  # 1 m
        solute_mw = 58.44  # NaCl molecular weight
        
        molarity = self.converter.molality_to_molarity(molality, solute_mw)
        
        # Should be a positive number
        self.assertGreater(molarity, 0)
        self.assertIsInstance(molarity, float)
    
    def test_molarity_to_normality(self):
        """Test molarity to normality conversion."""
        molarity = 2.0  # 2 M
        solute_mw = 36.46  # HCl molecular weight
        valence_factor = 1
        
        normality = self.converter.molarity_to_normality(molarity, solute_mw, valence_factor)
        
        # Should equal molarity * valence_factor
        expected = molarity * valence_factor
        self.assertEqual(normality, expected)
    
    def test_normality_to_molarity(self):
        """Test normality to molarity conversion."""
        normality = 2.0  # 2 N
        solute_mw = 36.46  # HCl molecular weight
        valence_factor = 1
        
        molarity = self.converter.normality_to_molarity(normality, solute_mw, valence_factor)
        
        # Should equal normality / valence_factor
        expected = normality / valence_factor
        self.assertEqual(molarity, expected)
    
    def test_calculate_mass_percent(self):
        """Test mass percent calculation."""
        molarity = 1.0  # 1 M
        solute_mw = 58.44  # NaCl molecular weight
        
        mass_percent = self.converter.calculate_mass_percent(molarity, solute_mw)
        
        # Should be between 0 and 100
        self.assertGreater(mass_percent, 0)
        self.assertLess(mass_percent, 100)
        self.assertIsInstance(mass_percent, float)
    
    def test_calculate_molarity_from_mass_percent(self):
        """Test molarity calculation from mass percent."""
        mass_percent = 5.0  # 5%
        solute_mw = 58.44  # NaCl molecular weight
        
        molarity = self.converter.calculate_molarity_from_mass_percent(mass_percent, solute_mw)
        
        # Should be a positive number
        self.assertGreater(molarity, 0)
        self.assertIsInstance(molarity, float)
    
    def test_calculate_parts_per_million(self):
        """Test parts per million calculation."""
        molarity = 0.001  # 0.001 M
        solute_mw = 58.44  # NaCl molecular weight
        
        ppm = self.converter.calculate_parts_per_million(molarity, solute_mw)
        
        # Should be a positive number
        self.assertGreater(ppm, 0)
        self.assertIsInstance(ppm, float)
    
    def test_invalid_parameters(self):
        """Test that invalid parameters raise appropriate errors."""
        # Negative molarity
        with self.assertRaises(ValueError):
            self.converter.molarity_to_molality(-1.0, 58.44)
        
        # Negative molecular weight
        with self.assertRaises(ValueError):
            self.converter.molarity_to_molality(1.0, -58.44)
        
        # Zero molecular weight
        with self.assertRaises(ValueError):
            self.converter.molarity_to_molality(1.0, 0)
        
        # Negative normality
        with self.assertRaises(ValueError):
            self.converter.normality_to_molarity(-1.0, 58.44)
        
        # Invalid valence factor
        with self.assertRaises(ValueError):
            self.converter.molarity_to_normality(1.0, 58.44, 0)
    
    def test_get_conversion_analysis(self):
        """Test getting comprehensive conversion analysis."""
        analysis = self.converter.get_conversion_analysis('M', 'm', 1.0, 58.44)
        
        self.assertEqual(analysis['from_unit'], 'M')
        self.assertEqual(analysis['to_unit'], 'm')
        self.assertEqual(analysis['original_value'], 1.0)
        self.assertIsInstance(analysis['converted_value'], float)
        self.assertEqual(analysis['solute_mw'], 58.44)
        self.assertTrue(analysis['is_valid'])
        self.assertIsNone(analysis['error'])
        self.assertIsInstance(analysis['conversion_steps'], list)
    
    def test_get_conversion_analysis_invalid(self):
        """Test getting analysis for invalid conversion."""
        analysis = self.converter.get_conversion_analysis('M', 'invalid', 1.0, 58.44)
        
        self.assertEqual(analysis['from_unit'], 'M')
        self.assertEqual(analysis['to_unit'], 'invalid')
        self.assertEqual(analysis['original_value'], 1.0)
        self.assertIsNone(analysis['converted_value'])
        self.assertEqual(analysis['solute_mw'], 58.44)
        self.assertFalse(analysis['is_valid'])
        self.assertIsNotNone(analysis['error'])
        self.assertEqual(analysis['conversion_steps'], [])
    
    def test_get_solvent_density(self):
        """Test getting solvent density."""
        # Test water
        density = self.converter.get_solvent_density('water')
        self.assertEqual(density, 0.997)
        
        # Test ethanol
        density = self.converter.get_solvent_density('ethanol')
        self.assertEqual(density, 0.789)
        
        # Test unknown solvent
        with self.assertRaises(ValueError):
            self.converter.get_solvent_density('unknown')
    
    def test_list_available_solvents(self):
        """Test listing available solvents."""
        solvents = self.converter.list_available_solvents()
        
        self.assertIsInstance(solvents, list)
        self.assertIn('water', solvents)
        self.assertIn('ethanol', solvents)
        self.assertIn('methanol', solvents)
    
    def test_round_trip_conversions(self):
        """Test round-trip conversions for consistency."""
        # Molarity to molality and back
        original_molarity = 1.0
        solute_mw = 58.44
        
        molality = self.converter.molarity_to_molality(original_molarity, solute_mw)
        converted_molarity = self.converter.molality_to_molarity(molality, solute_mw)
        
        # Should be close to original (within 1%)
        self.assertAlmostEqual(converted_molarity, original_molarity, delta=0.01)
    
    def test_mass_percent_round_trip(self):
        """Test round-trip mass percent conversions."""
        original_mass_percent = 5.0
        solute_mw = 58.44
        
        molarity = self.converter.calculate_molarity_from_mass_percent(original_mass_percent, solute_mw)
        converted_mass_percent = self.converter.calculate_mass_percent(molarity, solute_mw)
        
        # Should be close to original (within 1%)
        self.assertAlmostEqual(converted_mass_percent, original_mass_percent, delta=0.01)


if __name__ == '__main__':
    unittest.main() 
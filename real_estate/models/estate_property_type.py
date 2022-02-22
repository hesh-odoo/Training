from odoo import api,fields, models

class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order= "name"

    name = fields.Char(required=True)
    property_ids= fields.One2many("estate.property", "property_type")
    expected_price= fields.Float("estate.property", "expected_price")
    sequence= fields.Integer('Sequence', dafault=1)
    

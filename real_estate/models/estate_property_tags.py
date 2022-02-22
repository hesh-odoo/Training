from odoo import _,fields, models, api

class estate_property_tags(models.Model):
    _name ="estate.property.tags"
    _description= "Estate Property Tags"
    _order= "name"
    _sql_constraints = [('name_uniq', 'unique(name)', 'The Property Tag name must be unique')]

    name= fields.Char(required=True)
    color= fields.Integer("color")
  

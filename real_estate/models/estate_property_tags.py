from odoo import fields, models

class estate_property_tags(models.Model):
    #Model attributes
    _name = "estate.property.tags"
    _description = "Real Estate Proprtey Tags"
    _order="name,sequence"
    
    #Model Fields
    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. lsower is better.")
    color=fields.Integer()
    
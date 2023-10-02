from odoo import fields, models,api,exceptions

class estate_property_type(models.Model):
    #Model attributes
    _name = "estate.property.type"
    _description = "Define Property Type"
    _order="sequence,name"
    
    #Model Fields
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id',string="Property Ids")
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. lsower is better.")
    offer_count=fields.Integer(compute="_count_offers")
    
    #Model Reltional Fields
    offer_ids=fields.One2many('estate.property.offer','property_type_id',string="Type offer list")
    
    #Model Functions
    def _count_offers(self):
        for record in self:
            record.offer_count=len(record.offer_ids)
            

            

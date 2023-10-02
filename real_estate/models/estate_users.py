from odoo import models,fields
class estate_users(models.Model):
    #Model attributes
    _inherit = 'res.users'
    #Model fields
    property_ids = fields.One2many('estate.property','user_id',string="Properties")
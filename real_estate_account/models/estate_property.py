from odoo import models
class estate_property(models.Model):
    #Model attributes
    _name = "estate.property"
    _description = "Linking Module"
    _inherit ="estate.property"
    
    #Model Functions
    def sold_property_button(self):
        res = super().sold_property_button()
        if res: # if property SOLD
            #creates accounting journal of type sale
            journal = self.env['account.move'].with_context(default_move_type='out_invoice').sudo()._get_default_journal()
            #create account move with partner id, move type, journal id, and invoice line ids
            self.env['account.move'].sudo().create({
                'partner_id':self.partner_id,
                'move_type':'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    (0,0,
                     {
                        'name':'Available property',
                        'quantity': 1,
                        'price_unit': self.selling_price*0.06
                    }),
                    (0,0,
                     {
                        'name':'Administrative fees',
                        'quantity':1,
                        'price_unit':100
                    })
                ]
            })
        
    
from odoo import fields, models,api,exceptions,tools
import datetime

class estate_property_offer(models.Model):
    #Model attributes
    _name = "estate.property.offer"
    _description = "Real Estate Proprtey Offer"
    _order="price desc"
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)','The offer price should be strictly positive.')
    ]
    
    #Model Fields
    price=fields.Float()
    status = fields.Selection(
        string="offer status",
        selection=[('accepted','Accepted'),('refused','Refused')],
        help="Offer status is uesed to show the offer's status",
        copy=False
    )
    validity=fields.Integer(default='7')
    date_deadline=fields.Date(compute="_compute_date_deadline",inverse="_inverse_date_deadline")
    
    #Reltional Fields
    partner_id=fields.Many2one('res.partner',string="Partner",required=True)
    property_id=fields.Many2one('estate.property',required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store = True) #store means store in DB
    
    
    #Model Functions
    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if record.create_date else datetime.date.today()) +datetime.timedelta(days = record.validity)
            
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline-record.create_date.date()).days
            
    def accept_offer_button(self):
        for record in self:
            self._reset_offers_status(record.property_id)
            record.status = 'accepted'
            record.property_id.selling_price= record.price #property selling price = offer price
            record.property_id.partner_id = record.partner_id #property buyer = offer partner
            record.property_id.state = 'accepted' #proprter state accpted
        return True
    
    def refuse_offer_button(self):
        for record in self:
            if record.status == 'accepted':
                self._reset_property_id(record) #set price and buyer to null
            record.status = 'refused' #then refuse the offer
            record.property_id.state= 'received' #set the state to offer recived
        return True
    
    #this function will refuse an offer once another is accepted
    def _reset_offers_status(self,property_id):
        for record in property_id.offer_ids:
            if record.status == 'accepted':
                record.status = 'refused'
    
    def _reset_property_id(self,record):
        record.property_id.selling_price= 0
        record.property_id.partner_id = None
    
    @api.model
    def create(self,vals):
        estate_property = self.env['estate.property'].browse(vals['property_id'])
        if tools.float_compare(estate_property.best_offer,vals['price'],precision_digits=3)>=0:
            raise exceptions.UserError("The offer must be higher than current best offer")
        estate_property.state='received'
        return super().create(vals) #Inherited functions always return itself
        
    
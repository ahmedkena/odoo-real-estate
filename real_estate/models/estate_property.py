from odoo import fields, models,api,exceptions,tools,_
from decimal import *
class estate_property(models.Model):
    #Model attributes
    _name = "estate.property"
    _description = "Real Estate Proprtey Managmment System"
    _order="id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)','The expected price should be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)','The selling price should be strictly positive.')
    ]
    
    #Model fields
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price= fields.Float()
    bedrooms = fields.Integer(default='2')
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='garden_orientation',
        selection= [('north','North'),('south','South'),('east','East'),('west','West')],
        help="Orientation is used to info the orientation of the garden"

    )
    state = fields.Selection(
        string="State",
        copy=False,
        selection= [('new','NEW'),('received','OFFER RECEIVED'),('accepted','OFFER ACCEPTED'),('sold','SOLD'),('canceled','CANCELD')],
        default= 'new'
    )
    status = fields.Selection(
        string="Status",
        selection= [('new','New'),('canceled','Canceled'),('sold','Sold')],
        default = 'new'
    )
    total_area=fields.Integer(compute='_compute_total_area',readonly='True')
    best_offer=fields.Float(compute='_compute_best_price',readonly='True')
    company_id=fields.Integer(required=True,default=lambda self:self.env.company.id )
    #Model reltional fields
    property_type_id= fields.Many2one("estate.property.type",string="Property type")
    user_id= fields.Many2one('res.users',string="Salesman",index=True,default=lambda self:self.env.user) #self:self.env.user = the current user
    partner_id = fields.Many2one('res.partner',string="Buyer",index= True,copy = False)
    tag_ids=fields.Many2many('estate.property.tags',string="tags")
    offer_ids = fields.One2many('estate.property.offer',"property_id",string="Offers")

    #Model Functions
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area= record.living_area+record.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids)>0:
                record.best_offer= max(record.offer_ids.mapped('price'))
            else:
                record.best_offer=0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation='north'
        else:
            self.garden_area = 0
            self.garden_orientation = ""
            
    def cancel_property_button(self):
        for record in self:
            if record.status == 'new':
                record.status='canceled'
                record.state='canceled'
                return True
            elif record.status == 'canceled':
                raise exceptions.UserError("Property alredy canceld")
            else:
                raise exceptions.UserError("Cannost Cancel a sold Property")
        return True
    
    def sold_property_button(self):
        for record in self:
            if record.status == 'new':
                record.status='sold'
                record.state='sold'
                return True
            elif record.status == 'canceled':
                raise exceptions.UserError("Cannot sell a Canceled Property")
            else:
                raise exceptions.UserError("This property alredy sold")
        return True
    
    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for record in self:
            min_selling_price= float(Decimal(record.expected_price)*Decimal(0.9)) 
            #Decimal function does floating to the numbers
            compared_result= tools.float_compare(record.selling_price,min_selling_price,precision_digits=3)
            #float_compare returns 0 if values are equal,
            #returns 1 if first value is bigger, return -1 if second value is bigger
            if (not tools.float_is_zero(record.selling_price,precision_digits=3)) and (compared_result < 0):
                raise exceptions.ValidationError(_('The selling price cannot be lower than 90 percent of the expected price.'))
            
    def unlink(self):
        for record in self:
            if  not(record.state=='new' or record.state =='canceled'):
                raise exceptions.UserError('Only new and canceled property can be deleted')
        return super().unlink()
            
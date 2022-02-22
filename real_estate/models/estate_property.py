from odoo import api, fields, models
from odoo.exceptions import UserError

class estate_property(models.Model):
    _name = "estate.property"
    _description = "Real Esate Property"
    _order = "id desc"
    _sql_constraints=[('check_selling_price', 'check(selling_price >= 0)', 'The Selling price must be in Positive'),
                      ('name_uniq', 'UNIQUE (name)', 'The Property name must be unique'),
                      ('check_expected_price', 'check(expected_price >= 0 )', 'The Expected price must be in Positive.'),]


    name = fields.Char(help="Propety Name", required=True)
    description = fields.Text(help="Property Details")
    postcode = fields.Char(help="Postal Code")
    date_availability = fields.Date(help="date at which you will be available. It can't be more than 3 months", copy=False)
    expected_price =  fields.Float(help="Expected price", required=True)
    best_price= fields.Float(help="Best Price offered", string="Best Price", compute="_compute_best_price")
    selling_price =  fields.Float(help="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(help="No of Rooms", default="2")
    living_area = fields.Integer(help="Size of living area in Sqm", string="Living Area(Sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(help="Size of garden area in Sqm", string="Garden Area(Sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation", 
    selection=[ ("north","North"),
                ("south","South"),
                ("east","East"),
                ("west","West")])

    total_area= fields.Float(help="Total area of property", string="Total Area", compute='_compute_total_area')
    active = fields.Boolean(default = True)
    state = fields.Selection(string="State of the property", required=True, copy=False, default="new", 
    selection=[ ("new","New"),
                ("offer_received","Offer Received"),
                ("offer_accepted","Offer Accepted"),
                ("sold","Sold"),
                ("cancel","Cancel")])
    type_ids= fields.One2many('estate.property.type','id', string="Property Id")
    property_type= fields.Many2one('estate.property.type', string="Property Type")
    buyer= fields.Many2one('res.partner', string="Buyer", copy=False)
    seller= fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids= fields.Many2many('estate.property.tags', string='Tags')
    offer_ids= fields.One2many('estate.property.offers', 'property_id', string='Offers')
    

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = 0
            if record.offer_ids:
                record.best_price =max (record.offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_orientation = 'north'
            self.garden_area = '10'
        else:
            self.garden_orientation = ''
            self.garden_area = '0'

    def sold_property(self):
        for record in self:
            if record.state == 'cancel':
                raise UserError("Canelled property can not be sold.")
            record.state = "sold"
        return True

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property can not be cancelled.")
            record.state = "cancel"
        return True

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            x=0
            for offer in record.offer_ids:
                if offer.price > x:
                    x = offer.price
            record.best_price = x

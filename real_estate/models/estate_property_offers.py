from odoo import api,fields, models
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import UserError

class estate_property_offers(models.Model):
    _name="estate.property.offers"
    _description="Property Offers"
    _order="price desc"

    price= fields.Float(help='Offer Price')
    validity= fields.Integer(string='Validity (days)', default=7)
    date_deadline= fields.Datetime(string='Deadline', compute='_compute_validity_offer', inverse='_inverse_validity_offer')
    status= fields.Selection(string="Offer Status", copy=False,
    selection=[("accepted","Accepted"),
               ("refused", "Refused")])
    partner_id= fields.Many2one('res.partner', string="Partner Id", required=True)
    property_id= fields.Many2one('estate.property', string="Property Id", required=True)

    @api.constrains("price")
    def check_price(self):
        for record in (self):
            x = record.property_id.expected_price
            c = (x*90)/100
            if not record.price>=c:
                raise UserError("The offer must be 90%% of expected price")
    

    @api.depends('validity', 'create_date')
    def _compute_validity_offer(self):
        for record in self:
            if record.create_date:
                record.date_deadline= record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline= fields.date.today() + relativedelta(days=record.validity)

    def _inverse_validity_offer(self):
        for record in self:
            if record.validity:
                validity_difference = record.date_deadline - record.create_date
                record.validity = validity_difference.days + 1
            else:
                record.validity = 7

    def action_accept(self):
        for record in self:
            if record.status == 'refused':
                raise UserError("Refused offer cannot be accepted.")
            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("Accepted offer cannot be refused.")
            record.status = "refused"
        return True

    
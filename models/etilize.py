# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EtilizeAttributeMaster(models.Model):
    _inherit = 'etilize.attribute.master'

    # Add indexes

    # Add fields
    sequence = fields.Integer(default=10)

    filter_ok = fields.Boolean(
        'Filter',
        index=True,
        help="If true, a website filter will be shown.",
    )

    filter_group_id = fields.Many2one(
        'product.filter.group',
        index=True,
        string="Filter Group",
    )

    filter_type = fields.Selection([
        ('radio', 'Radio'),
        ('select', 'Select'),
        ('color', 'Color'),
        ('hidden', 'Hidden'),
        ],
        default='radio',
    )

    type_variant = fields.Selection([('radio', 'Radio'),('select', 'Select'),('color', 'Color'),('hidden', 'Hiden')], 'Typer Variant')
    is_variant = fields.Boolean('Is variant')

class EtilizeAttributeValueMaster(models.Model):
    _inherit = "etilize.attribute.value.master"

    # Add Indexes
    name = fields.Char(index=True)
    etilize_attribute_id = fields.Many2one(index=True)

    sequence = fields.Integer(default=10)
    filter_html_color = fields.Char(
        string='HTML Color Index',
        help="Here you can set a specific HTML color index (e.g. #ff0000) "
             "to display the color on the website if the attibute type is "
             "'Color'."
    )

class EtilizeAttributeMatching(models.Model):
    _inherit = "etilize.attribute.matching"

    # Add indexes
    prod_etilize_attr_match = fields.Many2one(index=True)
    etilize_attribute_values = fields.Many2many(index=True)

    filter_ok = fields.Boolean(related='etilize_attribute_id.filter_ok')

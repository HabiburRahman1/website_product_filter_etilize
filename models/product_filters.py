# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class ProductFilters(models.Model):
    _inherit = "product.filter"
    _table = 'product_filter_etilize_view'
    _auto = False

    name = fields.Char(readonly=True)
    group_id = fields.Many2one(readonly=True)
    value_ids = fields.One2many(readonly=True)
    sequence = fields.Integer(readonly=True)
    filter_line_ids = fields.One2many(readonly=True)
    create_variant = fields.Boolean(readonly=True)
    type = fields.Selection(readonly=True)

    _sql_constraints = []


    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'product_filter_etilize_view')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW product_filter_etilize_view AS (
            SELECT 
                -- Basics, copy from master
                id,
                create_date,
                create_uid,
                write_date,
                write_uid,
                -- Transformed
                name                    AS name,
                filter_group_id         AS group_id,
                sequence                AS sequence,
                FALSE                   AS create_variant, -- TODO?
                filter_type             AS type
                -- value_ids is One2Many
                -- filter_line_ids is One2Many
            FROM etilize_attribute_master
            WHERE filter_ok = True
        )""")    


class ProductFiltervalue(models.Model):
    _inherit = "product.filter.value"
    _table = 'product_filter_value_etilize_view'
    _auto = False

    name = fields.Char(readonly=True)
    sequence = fields.Integer(readonly=True)
    filter_id = fields.Many2one(readonly=True)
    html_color = fields.Char(readonly=True)

    _sql_constraints = []


    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'product_filter_value_etilize_view')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW product_filter_value_etilize_view AS (
            SELECT 
                -- Basics, copy from master
                eav.id,
                eav.create_date,
                eav.create_uid,
                eav.write_date,
                eav.write_uid,
                -- Transformed
                eav.name                    AS name,
                eav.sequence                AS sequence,
                eav.etilize_attribute_id    AS filter_id,
                eav.filter_html_color       AS html_color
                -- product_ids is Many2many
            FROM etilize_attribute_value_master eav
            LEFT JOIN etilize_attribute_master ea ON (eav.etilize_attribute_id = ea.id)
            WHERE ea.filter_ok = True
            --AND eav.id IN (SELECT attribute_val_id FROM etilize_attribute_value_product_rel)
        )""")


class ProductfilterLine(models.Model):
    _inherit = "product.filter.line"
    _table = 'product_filter_line_etilize_view'
    _auto = False

    product_tmpl_id = fields.Many2one(readonly=True)
    filter_id = fields.Many2one(readonly=True)

    # use the same table as etilize 'etilize_attribute_value_product_rel', 'attribute_val_id', 'product_id'
    value_ids = fields.Many2many(
        relation='etilize_attribute_value_product_rel',
        column1='attribute_val_id',
        column2='product_id',
        readonly=True,
    )


    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'product_filter_line_etilize_view')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW product_filter_line_etilize_view AS (
            SELECT 
                -- Basics, copy from master
                eam.id,
                eam.create_date,
                eam.create_uid,
                eam.write_date,
                eam.write_uid,
                -- Transformed
                eam.prod_etilize_attr_match AS product_tmpl_id,
                eam.etilize_attribute_id    AS filter_id
                -- value_ids is Many2many
            FROM etilize_attribute_matching eam
            LEFT JOIN etilize_attribute_master ea ON (eam.etilize_attribute_id = ea.id)
            WHERE ea.filter_ok = True
        )""")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    filter_line_ids = fields.One2many(readonly=True)

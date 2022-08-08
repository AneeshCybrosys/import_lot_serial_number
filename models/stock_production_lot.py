# -*- coding: utf-8 -*-
from odoo import models, fields
import openpyxl
import zipfile
import base64
from io import BytesIO
from odoo.exceptions import UserError


class StockProductionLotInherit(models.Model):
    _inherit = 'stock.production.lot'

    def import_button(self):
        return {
            'name': 'ADD The Xls file',
            'type': 'ir.actions.act_window',
            'res_model': 'import.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new'
        }


class ImportWizard(models.TransientModel):
    _name = 'import.wizard'
    _description = 'Import wizard'

    attachment = fields.Binary(string="Attachment")
    attachment_name = fields.Char(string='Attachment Name')

    def attachment_button(self):
        try:
            wb = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.attachment)),
                read_only=True)
            ws = wb.active
            for row in ws.iter_rows(min_row=2, max_row=None, min_col=None,
                                    max_col=None, values_only=True):
                search = self.env['product.product'].search(
                    [('name', '=', row[2])])
                if not search:
                    new = self.env['product.product'].create({
                        'name': row[2],
                        'detailed_type': 'product'
                    })
                    self.env['stock.production.lot'].create({
                        'name': row[0],
                        'product_id': new.id,
                        'company_id': self.env.user.company_id.id
                    })
                else:
                    self.env['stock.production.lot'].create({
                        'name': row[0],
                        'product_id': search.id,
                        'company_id': self.env.user.company_id.id
                    })
            return {
                'name': 'Success',
                'type': 'ir.actions.act_window',
                'res_model': 'success.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new'
            }

        except TypeError:
            raise UserError('Select a file')
        except zipfile.BadZipFile:
            raise UserError('Only excel files are supported.')


class SuccessWizard(models.TransientModel):
    _name = 'success.wizard'
    _description = 'Success wizard'

    message = fields.Text(default="Success", readonly=True)

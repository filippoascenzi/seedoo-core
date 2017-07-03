# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp import SUPERUSER_ID

class protocollo_config_settings(osv.osv_memory):
    _name = 'protocollo.config.settings'
    _inherit = 'res.config.settings'

    _columns = {
        'config_id': fields.many2one('protocollo.configurazione', string='Configurazione', required=True),

        'genera_segnatura': fields.related('config_id', 'genera_segnatura', type='boolean', string='Genera Segnatura nel PDF'),
        'genera_xml_segnatura': fields.related('config_id', 'genera_xml_segnatura', type='boolean', string='Genera XML Segnatura'),
    }

    def _default_config_id(self, cr, uid, context):
        ir_model_data_obj = self.pool.get('ir.model.data')
        ir_model_data_id = ir_model_data_obj.search(cr, uid, [('name', '=', 'configurazione_protocollo_default')])[0]
        ir_model_data = ir_model_data_obj.browse(cr, uid, ir_model_data_id)
        return ir_model_data.res_id

    _defaults = {
        'config_id': lambda self,cr,uid,c: self._default_config_id(cr, uid, c),
    }

    def on_change_config_id(self, cr, uid, ids, config_id, context=None):
        config_data = self.pool.get('protocollo.configurazione').read(cr, uid, [config_id], [], context=context)[0]
        values = {}
        for fname, v in config_data.items():
            if fname in self._columns:
                values[fname] = v[0] if v and self._columns[fname]._type == 'many2one' else v
        return {'value': values}


    # FIXME in trunk for god sake. Change the fields above to fields.char instead of fields.related,
    # and create the function set_website who will set the value on the website_id
    # create does not forward the values to the related many2one. Write does.
    def create(self, cr, uid, vals, context=None):
        config_id = super(protocollo_config_settings, self).create(cr, SUPERUSER_ID, vals, context=context)
        self.write(cr, SUPERUSER_ID, config_id, vals, context=context)
        return config_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

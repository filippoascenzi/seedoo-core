# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class dematerializzazione_importa_documenti_step1_wizard(osv.TransientModel):
    _name = 'dematerializzazione.importa.documenti.step1.wizard'
    _description = 'Wizard di Importazione Documenti: STEP 1'

    _columns = {
        'verifica_importer': fields.boolean(
            'Verifica Importer',
        ),
        'importer_ids': fields.one2many(
            'dematerializzazione.importa.documenti.imp.step1.wizard',
            'wizard_id',
            'Importer'),
    }

    def _default_importers(self, cr, uid, context):
        importer_obj = self.pool.get('dematerializzazione.importer')
        importer_ids = importer_obj.search(cr, uid, [('import_attivo', '=', True)])
        importers = importer_obj.browse(cr, uid, importer_ids)
        return importers

    def _default_verifica_importer(self, cr, uid, context):
        importers = self._default_importers(cr, uid, context)
        return len(importers)


    def _default_importer_ids(self, cr, uid, context):
        importers = self._default_importers(cr, uid, context)
        res = []
        for importer in importers:
            res.append({
                'title': importer.title,
                'description': importer.description,
                'address': importer.address,
            })
        return res

    _defaults = {
        'verifica_importer': _default_verifica_importer,
        'importer_ids': _default_importer_ids
    }

    def step2(self, cr, uid, ids, context=None):
        importer_obj = self.pool.get('dematerializzazione.importer')
        storico_id = importer_obj.importa_documenti(cr, uid, 'manuale')
        context['storico_id'] = storico_id

        return {
            'name': _('Wizard di Importazione Documenti: STEP 2'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'dematerializzazione.importa.documenti.step2.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context
        }


class dematerializzazione_importa_documenti_imp_step1_wizard(osv.TransientModel):
    _name = 'dematerializzazione.importa.documenti.imp.step1.wizard'
    _columns = {
        'wizard_id': fields.many2one('dematerializzazione.importa.documenti.step1.wizard'),
        'title': fields.char('Nome', char=80, required=True),
        'description': fields.text('Descrizione'),
        'address': fields.char('Indirizzo', char=256, required=True),
    }


class dematerializzazione_importa_documenti_step2_wizard(osv.TransientModel):
    _name = 'dematerializzazione.importa.documenti.step2.wizard'
    _description = 'Wizard di Importazione Documenti: Esito'

    ESITO_SELECTION = [('ok', 'OK'), ('errore', 'Errore')]

    _columns = {
        'esito': fields.selection(ESITO_SELECTION, 'Esito', select=True),
        'numero_file_importati': fields.integer('Numero File Importati'),
        'numero_file_errore': fields.integer('Numero File in Errore')
    }

    def _default_storico(self, cr, uid, context=None):
        if context is None:
            context = {}
        if context.has_key('storico_id') and context['storico_id']:
            storico_obj = self.pool.get('dematerializzazione.storico.importazione')
            storico = storico_obj.browse(cr, uid, context['storico_id'])
            return storico
        return None

    def _default_esito(self, cr, uid, context=None):
        storico = self._default_storico(cr, uid, context)
        if storico:
            return storico.esito
        else:
            return 'errore'

    def _default_numero_file_importati(self, cr, uid, context=None):
        storico = self._default_storico(cr, uid, context)
        if storico:
            return storico.numero_file_importati
        else:
            return 0

    def _default_numero_file_errore(self, cr, uid, context=None):
        storico = self._default_storico(cr, uid, context)
        if storico:
            return storico.numero_file_errore
        else:
            return 0

    _defaults = {
        'esito': _default_esito,
        'numero_file_importati': _default_numero_file_importati,
        'numero_file_errore': _default_numero_file_errore
    }

    def go_to_history(self, cr, uid, ids, context=None):

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'dematerializzazione.storico.importazione',
            'res_id': context['storico_id'],
            'type': 'ir.actions.act_window',
            'context': context,
        }
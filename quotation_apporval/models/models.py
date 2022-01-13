# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class quotation_apporval(models.Model):
    _inherit = 'sale.order'

    email_sent = fields.Boolean("Email sent", default=False)
    num_days = fields.Integer("Number Days")
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('op', 'OM Approval'),
        ('md', 'MD Approval'),
        ('approval', 'Approved Quatation'),
        ('sent', 'Quotation Sent'),
        ('accountant', 'Accountant Approval'),
        ('sale', 'Sales Order'),
        ('cancel', 'Cancelled'),
    ], string='Status',index=True, tracking=3, default='draft')

    def submit(self):
        # user_group = self.env.ref("quotation_apporval.om_approval_security")
        # om_user = [usr.partner_id.email for usr in user_group.users if usr.partner_id.email]
        # all_users = [om_user]
        # for email in all_users:
        #     for i in email:
        #         template_rec = self.env.ref('quotation_apporval.mail_template_send_to_om_approval')
        #         template_rec.write({'email_to': i})
        #         template_rec.send_mail(self.id, force_send=True)
        for rec in self:
            rec.state = 'op'

    def reject(self):
        for rec in self:
            rec.state = 'op'

    def approve(self):
        user_group = self.env.ref("quotation_apporval.md_approval_security")
        md_user = [usr.partner_id.email for usr in user_group.users if usr.partner_id.email]
        all_users = [md_user]
        for email in all_users:
            for i in email:
                template_rec = self.env.ref('quotation_apporval.mail_template_send_to_md_approval')
                template_rec.write({'email_to': i})
                template_rec.send_mail(self.id, force_send=True)
        for rec in self:
            rec.state = 'md'

    def approve_accountant(self):
        user_group = self.env.ref("quotation_apporval.accountant_approval_security")
        accountant_user = [usr.partner_id.email for usr in user_group.users if usr.partner_id.email]
        all_users = [accountant_user]
        for email in all_users:
            for i in email:
                template_rec = self.env.ref('quotation_apporval.mail_template_send_to_accountant_approval')
                template_rec.write({'email_to': i})
                template_rec.send_mail(self.id, force_send=True)
        for rec in self:
            a = rec.payment_term_id.display_name
            payment_check = rec.payment_term_id.advance_payment_check

            if payment_check:
                if not rec.po_copy:
                    raise UserError(_("Please Attach  Po Copy"))
                elif not rec.cheque_copy:
                    raise UserError(_("Please Attach Cheque Copy "))
                rec.state = 'accountant'
            elif a == 'cash':
                if not rec.po_copy:
                    raise UserError(_("Please Attach  Po Copy "))
                rec.action_confirm()
                rec.state = 'sale'
            else:
                rec.state = 'accountant'

    def approve_id(self):
        for rec in self:
            a = rec.payment_term_id.display_name
            if a == 'cash':
                rec.state = 'approval'
            else:
                rec.state = 'approval'

    def send_pro_forma(self):
        for rec in self:
            rec.state = 'approval'
    def apporved(self):
        for rec in self:
            rec.state = 'accountant'

    def reject_send_to_om(self):
        for rec in self:
            rec.state = 'accountant'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_quotation_send(self):
        for rec in self:
            rec.email_sent = True
            # rec.state = 'accountant'
        return super(quotation_apporval, self).action_quotation_send()

    def action_confirm(self):
        res = super(quotation_apporval, self).action_confirm()
        for rec in self:
            rec.state = 'sale'
        return res

    @api.onchange('payment_term_id')
    def _onchange_payment_term_id(self):
        for rec in self:
            for payment in rec.payment_term_id.line_ids:
                rec.num_days = payment.days

# -*- coding: utf-8 -*-

###################################################################################
#

#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

{
    'name': 'Hide Product Cost Price',
    'summary': """Product Cost Price Will be Visible Only for Specified Group""",
    'version': '13.0.1.0.0',
    'description': """Product cost price will be visible only for specified group""",
    'author': 'Rightechs Solutions',
    'company': 'Rightechs Solutions',
    'website': 'https://www.rightechs.info',
    'category': 'Extra Tools',
    'depends': ['base', 'product','sale','stock_account'],
    'license': 'AGPL-3',
    'data': [
        'security/view_cost_price.xml',
        'views/hide_product_cost.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,

}

odoo.define('sofid_sale.IntegerOnlyWidget', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');

    var IntegerOnlyWidget = AbstractField.extend({
        supportedFieldTypes: ['float'],
        
        events: {
            "input input": "_onInputChange",
            "focusin input": "_onFocus",
            "click input": "_onClickFocus"
        },

        _setFocus: function(){
            let input = this.$('input')[0];  
            setTimeout(() => {
                input.focus(); 
                input.setSelectionRange(input.value.length, input.value.length);
            }, 100);
        },
        _renderEdit: function () {
            this.$el.html('<input type="text" class="o_input" value="' + (this.value || '') + '"/>');
            this._setFocus()
            this._super(...arguments)
        },

        _onInputChange: function (event) {
            var value = event.target.value;
            if (!/^-?\d+$/.test(value) && value !== "") {
                value = value.slice(0, -1);
                event.target.value = value || ""; 
            }
            this._setValue(value);
        },
        _onFocus: function () {
            this._setFocus()
        },
        _onClickFocus: function () {
            let input = this.$('input')[0];
            if (input) {
                input.focus();
                input.setSelectionRange(input.value.length, input.value.length);
            }
        },
        _renderReadonly: function () {
            this.$el.text(this.value || ""); 
        },
   
    });

    fieldRegistry.add('integer_only', IntegerOnlyWidget);
});
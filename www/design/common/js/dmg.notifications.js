(function($) {
    $.jGrowl.defaults.closerTemplate = '<div>hide all notifications</div>';

    $.extend({
        notification: function(status, msg) {
            var header = null;
            var theme = status;
            var sticky = false;
            var msgformated = msg.replace( /\n/g, '<br />\n' );
            switch (theme) {
                case 'success':
                    header = "Success";
                    break;
                case 'info':
                    header = "Information";
                    sticky = true;
                    break;
                case 'error':
                    header = "Error";
                    sticky = true;
                    break;
                case 'warning':
                    header = "Warning";
                    break;
                case 'debug':
                    header = "Debug";
                    break;
            }    
            $.jGrowl(msgformated, { header: header, sticky: sticky, theme: theme });
        }
    });
})(jQuery);


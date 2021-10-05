function loadRecursive (context) {
    $("[data-autoload='true']", context).each(function (index, element) {
        var that = $(this);
        that.html(typeof that.data('loading') === 'undefined' ?  '<div class="loading">&nbsp;</div>' : that.attr('data-loading'));
        $.get(that.data('content-url'), function (data, textStatus) {
            response = $(data);
            that.html(response);
            loadRecursive(response);
        });
    });
};

$.fn.loadContent = function (force, url) {
    force = typeof force  === 'undefined' ? false : true;
    var target = this;
    /* pokud ma target element hodnotu data atributu 'toggle' nastavenu
     * na 'tab' (tzn. jedna se o element aktivujici/zobrazujci tab) nastavime
     * 'container' na element na ktery se odkazuje v atributu 'href' */
    if (target.data('toggle') == 'tab') {
        /* vyhledej prislusny container - element shodneho 'id' jako ma
         * target hodnotu atributu 'href' */
        container = $(target.attr('href'));
    } else {
        /* pokud target neni tabem, ale (napr.) "kolapsibilnim" panelem je
         * zaroven take sam containerem pro natazeni obsahu; pokud target
         * nedefinuje 'data-content-url' najdi a pouzij nejblizsi nadrazeny
         * element s timto atributem */
        if (typeof target.data('content-url') !== 'undefined' || typeof url !== 'undefined') {
            container = target;
        } else {
            container = target.closest('[data-content-url]');
        }
    }
    if (!container.hasClass('loaded') || force == true) {
        /* pokud container definuje data tribut min-height zobraz cekaci
         * kolecko dane minimalni vysky - v accordionu resi problem "blikani"
         * tabu pri obnove obsahu */
        container.html(typeof container.data('loading') === 'undefined' ?  '<div class="loading">&nbsp;</div>' : container.attr('data-loading'));
        /* natahni do 'container' elementu AJAXem URL z atributu 'data-content-url'
         * elementu 'target', pokud tento neni nadefinovany pokus se ho ziskat
         * z prislusneho 'container' elementu (v pripade ze natahujeme obsah tabu)
         * ve volani funkce loadContent (i reloadContent) lze "pretizit" URL
         * definovanou v data-content-url containeru/tabu (pouzito v nahravani
         * diskuzi k tvrenim v editacnim tabu u vyukove jednotky)
         */
        container.load(typeof url === 'undefined' ? target.data('content-url') ?
            target.data('content-url') :
            container.data('content-url') : url, function () {
            loadRecursive($(container));
        });
    }
};

$.fn.reloadContent = function (url) {
    this.loadContent(force=true, url);
};

$(document).ready(function () {
    $("[data-autoload='true']").each(function (index, element) {
        $(element).loadContent();
    });
    $(document).on('show.bs.collapse', 'div.panel-collapse', function (event) {
        if ($(this).children('div.panel-body[data-content-url]').length > 0) {
            $(this).children('div.panel-body[data-content-url]').loadContent();
        }
    });
    $(document).on('click', '.panel-actions .btn.reload', function (event) {
        $(this).closest('.panel').find('.panel-body[data-content-url]').reloadContent();
    });
    $(document).on('click', '.panel-actions .btn[data-content-url], .panel-action.btn[data-content-url]', function (event) {
        event.preventDefault()
        $(this).closest('.panel').find('.section-title').html($(this).data('section-title'));
        $(this).closest('.panel').find('.panel-body').data('content-url', $(this).data('content-url')).reloadContent();
        $(this).closest('.panel').find('.panel-collapse').collapse('show');
        event.stopPropagation();
        return false;
    });
});
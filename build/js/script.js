! function(e) {
    var t = {};

    function a(n) {
        if (t[n]) return t[n].exports;
        var i = t[n] = {
            i: n,
            l: !1,
            exports: {}
        };
        return e[n].call(i.exports, i, i.exports, a), i.l = !0, i.exports
    }
    a.m = e, a.c = t, a.d = function(e, t, n) {
        a.o(e, t) || Object.defineProperty(e, t, {
            enumerable: !0,
            get: n
        })
    }, a.r = function(e) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(e, "__esModule", {
            value: !0
        })
    }, a.t = function(e, t) {
        if (1 & t && (e = a(e)), 8 & t) return e;
        if (4 & t && "object" == typeof e && e && e.__esModule) return e;
        var n = Object.create(null);
        if (a.r(n), Object.defineProperty(n, "default", {
                enumerable: !0,
                value: e
            }), 2 & t && "string" != typeof e)
            for (var i in e) a.d(n, i, function(t) {
                return e[t]
            }.bind(null, i));
        return n
    }, a.n = function(e) {
        var t = e && e.__esModule ? function() {
            return e.default
        } : function() {
            return e
        };
        return a.d(t, "a", t), t
    }, a.o = function(e, t) {
        return Object.prototype.hasOwnProperty.call(e, t)
    }, a.p = "/", a(a.s = 1)
}({
    1: function(e, t, a) {
        e.exports = a("hB1A")
    },
    hB1A: function(e, t) {
        $(document).ready((function() {
            $("button.mobile-trigger").click((function() {
                $(this).toggleClass("active"), $(".mobile__navigation").toggleClass("active"), $(".header").toggleClass("active"), $("body").toggleClass("active")
            })), $(".mobile__navigation--main button").click((function() {
                $(this).hasClass("active__button") ? ($(this).removeClass("active__button"), $(this).siblings(".dropdown__menu").removeClass("active__menu")) : ($(this).addClass("active__button"), $(this).siblings(".dropdown__menu").toggleClass("active__menu"))
            }));
            var e = $(".dropdown__menu.active__menu ul li a");

            function t() {
                var e = $(".banner").outerHeight(),
                    t = $(".header");
                $(window).scrollTop() >= e ? (t.addClass("fixed_nav"), t.addClass("animated"), t.addClass("slideInDown")) : (t.removeClass("fixed_nav"), t.removeClass("animated"), t.removeClass("slideInDown"))
            }
            $(e).on("click", (function() {})), $((function() {
                $(window).scroll(t), t()
            })), window.location.hash && scroll(0, 0), setTimeout((function() {
                scroll(0, 0)
            }), 1), $((function() {
                $(".js-scroll-trigger").on("click", (function(e) {
                    $("html,body").animate({
                        scrollTop: $($(this).attr("href")).offset().top + "px"
                    }, 1e3, "swing")
                })), window.location.hash && $("html,body").animate({
                    scrollTop: $(window.location.hash).offset().top + -100
                }, 1e3, "swing")
            })), "CT" == $("select.state_select").val() && $("ct_opt").show(), $(".modal-open").click((function() {
                var e = $(this).attr("id");
                $("#modal-container").addClass(e).addClass("animation_in").removeClass("animation_out"), $("body").addClass("modal-active")
            })), $("#modal-container").click((function() {
                $(this).removeClass("animation_in").addClass("animation_out"), $("body").removeClass("modal-active")
            })), $(".modal-toggle").on("click", (function(e) {
                e.preventDefault(), console.log("toggle-modal function running"), $(".popup__form__modal .modal").toggleClass("is-visible"), $(".contact--form--popup").toggleClass("hidden")
            })), $(".popup__form__modal__wrapper .close__btn").on("click", (function() {
                $(".popup__form__modal .modal").removeClass("is-visible")
            })), $(".charter__request__form--trigger").on("click", (function(e) {
                e.preventDefault(), $(".charter__request__form__modal .modal").toggleClass("is-visible")
            })), $(".popup__form__modal__wrapper .close__btn").on("click", (function() {
                $(".charter__request__form__modal .modal").removeClass("is-visible")
            })), $(".modal-overlay").on("click", (function(e) {
                e.preventDefault(), $(".charter__request__form__modal .modal").removeClass("is-visible")
            })), $(".contact__disclaimer--btn").click((function() {
                $(this).siblings(".contact__disclaimer--text").toggleClass("visible", 300)
            })), $(".active-item .accordion__item__body").show(), $(".accordion__item__title").on("click", (function(e) {
                e.preventDefault();
                var t = $(this);
                t.parents(".faqs__section__accordion--item").hasClass("active-item") ? (t.parents(".faqs__section__accordion--item").removeClass("active-item"), $(this).siblings(".accordion__item__body").slideUp(300)) : ($(".faqs__section__accordion--item").removeClass("active-item"), t.parents(".faqs__section__accordion--item").addClass("active-item"), $(".accordion__item__body").slideUp(300), $(this).siblings(".accordion__item__body").slideDown(300))
            }));
            var a = $(".resources__slider--slider").flickity({
                    draggable: !0,
                    wrapAround: !0,
                    cellAlign: "left",
                    groupCells: 1,
                    prevNextButtons: !1,
                    pageDots: !1
                }),
                n = a.data("flickity"),
                i = $(".top__slider__nav");
            i.find(".slider__dot");
            a.on("select.flickity", (function() {
                $(".slider__dot").filter(".active").removeClass("active"), $(".slider__dot").eq(n.selectedIndex).addClass("active")
            })), i.on("click", ".slider__dot", (function() {
                var e = $(this).index();
                a.flickity("select", e)
            }));
            $(".inner__image__slider").flickity({
                draggable: ">1",
                wrapAround: !1,
                cellAlign: "center",
                prevNextButtons: !1,
                pageDots: !0,
                autoPlay: 3500
            }).data("flickity");
            $(".global__icon").click((function() {
                $(".language__buttons__menu").toggleClass("active")
            })), $(".language__button").click((function() {
                var e = $(this).attr("data-lang");
                $(".language__button").removeClass("active"), $(this).addClass("active");
                var t = $(this).data("text");
                $(".language_name").html(""), $(".global__icon").find(".language_name").html(t), $(".global__icon").find(".language_text").html(t), $(".language__buttons__menu").removeClass("active"), $(".language--change").each((function() {
                    $(this).attr("data-lang") === e ? ($(this).removeClass("hidden"), $(this).addClass("active-language")) : ($(this).removeClass("active-language"), $(this).addClass("hidden"))
                })), $(".toggle-language-content").each((function() {
                    $(this).attr("data-language") === e.toLowerCase() ? ($(this).removeClass("hidden"), $(this).addClass("active-language")) : ($(this).removeClass("active-language"), $(this).addClass("hidden"))
                }))
            })), $(".language--change, .blocks__item").each((function() {
                "Spanish" === $(this).attr("data-lang") && $(this).addClass("hidden")
            })), void 0 !== document.getElementsByClassName("goog-te-banner-frame skiptranslate")[0] && (document.getElementsByClassName("goog-te-banner-frame skiptranslate")[0].style.display = "none", document.body.style.top = "0px"), $(".testing__btn").click((function() {
                $('input[name="departure__type"]:checked').val()
            })), $("#calculate__route").submit((function(e) {
                e.preventDefault();
                var t = $("#saddr").val(),
                    a = $("#daddr").val(),
                    n = $('input[name="departure__type"]:checked').val(),
                    i = $("#date").val(),
                    o = $("#departure_time").val(),
                    s = ($("#preferred-route").val(), $("#transit_mode").val());
                encodeURIComponent(i + o);
                window.open("https://www.google.com/maps?saddr=" + t + "&daddr=" + a + "&ttype=" + n + "&date=" + i + "&time=" + o + "&dirflg=" + s)
            })), $(".route__btn").click((function() {
                $(".route__btn").removeClass("active"), $(this).addClass("active")
            })), $(".staff__nav__button:first-child, .citibus__staff__main__inner:first-child").addClass("active"), $(".staff__nav__button").click((function() {
                $(".staff__nav__button").removeClass("active"), $(this).addClass("active")
            })), $(".staff__nav__button").on("click", (function(e) {
                e.preventDefault();
                var t = $(this).attr("data-related");
                $(".citibus__staff__main__inner").each((function() {
                    $(this).hide(), $(this).addClass("active"), $(this).attr("id") == t && $(this).fadeIn()
                }))
            })), $(".special__links").each((function() {
                $(this).find(".bottom__links__wrapper .bottom__links__wrapper__column a").length >= 1 || $(this).hide()
            }))
        }))
    }
});

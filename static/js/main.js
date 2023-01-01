$(document).ready(() => {
  // Clipboard set up

  new ClipboardJS(".clipboard-copy");

  // Shorten Button Handler

  let fetching = false;

  const handleShortenClick = (e) => {
    e.preventDefault();

    if (fetching) return;

    const linkToShorten = $("#shorten-input").val().trim();

    // console.log(linkToShorten);

    // validate link

    $.ajax({
      url: "/ajax/shorten",

      beforeSend: (xhr) => {
        fetching = true;
        $(".loader").css({ display: "inline-block" });
        $(".shorten-text").hide();
      },

      type: "POST",
      dataType: "json",
      contentType: "application/json",
      processData: false,
      data: JSON.stringify({
        inputLink: linkToShorten,
        enableTracking: true,
        validity: 48,
        isCustom: false,
        author: null,
      }),
    })
      .done((json) => {
        // alert(json);

        $(".shorten-output").text(json.outputTarget);

        $(".pane-input").hide();
        $(".pane-output").slideDown();
      })
      .fail((xhr, status, error) => {
        alert(error);
      })
      .always((xhr, status) => {
        fetching = false;

        $(".loader").hide();
        $(".shorten-text").show();
      });
  };

  $(".shorten-btn").click(handleShortenClick);

  $(".restart").click((e) => {
    $("#shorten-input").val("");
    $(".pane-input").slideDown();
    $(".pane-output").hide();
  });

  $(".bi-clipboard").click((e) => {
    $(".bi-clipboard").hide();
    $(".bi-check2").show();

    const t = setTimeout(() => {
      $(".bi-clipboard").show();
      $(".bi-check2").hide();
      clearTimeout(t);
    }, 3000);
  });
});

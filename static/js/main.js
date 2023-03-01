function isValidUrl(url) {
  const typeOfUrl = typeof url;

  if (typeOfUrl !== "string") {
    throw new TypeError(`
      URL type is invalid. Expected a string, but got: ${typeOfUrl}
    `);
  }

  const protocol = "(?:(?:https?)://)";
  const ipv4 =
    "(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\.(?:[1-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))";
  const hostname = "(?:(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)";
  const domain =
    "(?:\\.(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)*";
  const tld = "(?:\\.(?:[a-z\\u00a1-\\uffff]{2,}))";
  const port = "(?::\\d{2,5})?";
  const resourcePath = "(?:[/?#]\\S*)?";
  const regex = `${protocol}(?:localhost|${ipv4}|${hostname}${domain}${tld}\\.?)${port}${resourcePath}`;
  const isUrl = new RegExp(`^${regex}$`, "i");

  return isUrl.test(url);
}

$(document).ready(() => {
  $(".custom-link-input").focus(() => {
    $(".custom-link-input-error").slideUp();
  });

  // SHow / Hide more options
  $(".show-options").click((e) => {
    // console.log("Showing...");
    $(".more-options").slideDown();
    $(".show-options").hide();
    $(".hide-options").show();
  });

  $(".hide-options").click((e) => {
    // console.log("Hiding...");

    $(".more-options").slideUp();
    $(".show-options").show();
    $(".hide-options").hide();
  });

  $(".mobile-menu-on").click((e) => {
    // console.log("Hiding...");

    $(".mobile-nav").slideDown();
    $(".mobile-menu-on").hide();
    $(".mobile-menu-off").show();
  });

  $(".mobile-menu-off").click((e) => {
    // console.log("Hiding...");

    $(".mobile-nav").slideUp();
    $(".mobile-menu-off").hide();
    $(".mobile-menu-on").show();
  });

  $(".custom-link-option").change((e) => {
    // console.log("Hiding...");

    const v = $(".custom-link-option").val();

    if (v === "1") {
      $(".custom-link-value").css({ display: "flex" });

      $(".custom-link-value").slideDown();
    } else if (v === "0") {
      $(".custom-link-value").slideUp();
    }
  });

  // Clipboard set up

  new ClipboardJS(".clipboard-copy");

  // Shorten Button Handler

  let fetching = false;

  const handleShortenClick = (e) => {
    e.preventDefault();

    if (fetching) return;

    const linkToShorten = $("#shorten-input").val().trim();

    // console.log(linkToShorten);

    if (!linkToShorten) {
      $(".pane-input-error").text("Fill in the link address.");
      $(".pane-input-error").slideDown();

      return;
    }

    let validity = $(".validity-input").val();
    let useCustomLink =
      $(".use-custom-link-input").val() === "1" ? true : false;
    let customLink = $(".custom-link-input").val().trim();

    if (!isValidUrl(linkToShorten)) {
      // alert("Invalid url");
      $(".pane-input-error").text("Uhm, that's not a valid link address.");
      $(".pane-input-error").slideDown();

      return;
    }

    // console.log(validity, useCustomLink, customLink);

    if (useCustomLink && (customLink.length < 3 || customLink > 24)) {
      // alert("Invalid url");
      $(".custom-link-input-error").text(
        "Custom link must be between 3 and 24 alphanumeric characters."
      );
      $(".custom-link-input-error").slideDown();

      $(".more-options").slideDown();
      $(".show-options").hide();
      $(".hide-options").show();

      return;
    }

    // validate link

    $.ajax({
      url: "/ajax/shorten",

      beforeSend: (xhr) => {
        fetching = true;
        $(".loader").css({ display: "inline-block" });
        $(".shorten-text").hide();
        $(".pane-input-error").hide();
      },
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      processData: false,
      data: JSON.stringify({
        inputLink: linkToShorten,
        enableTracking: true,
        isCustom: useCustomLink,
        author: null,
        validity: +validity.trim(),
        customLink: useCustomLink ? customLink : null,
      }),
    })
      .done((json) => {
        $(".pane-input-error").hide();

        $(".shorten-output").text(json.outputTarget);

        $(".pane-input").hide();
        $(".pane-output").slideDown();
      })
      .fail((xhr, status, error) => {
        // alert(xhr.status);

        if (useCustomLink) {
          // alert("Invalid url");
          $(".custom-link-input-error").text(
            `${xhr.responseJSON.detail || status}`
          );
          $(".custom-link-input-error").slideDown();

          $(".more-options").slideDown();
          $(".show-options").hide();
          $(".hide-options").show();
        }

        if (xhr.status === 422) {
          $(".pane-input-error").text("Invalid URL detected");
        } else {
          // console.log(xhr);
          $(".pane-input-error").text(`${xhr.responseJSON.detail || status}`);
        }
        $(".pane-input-error").slideDown();
        console.log(error);
      })
      .always((xhr, status) => {
        fetching = false;

        $(".loader").hide();
        $(".shorten-text").show();
      });
  };

  $(".shorten-btn").click(handleShortenClick);

  $("#shorten-input").focus(() => {
    $(".pane-input-error").hide();
  });

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

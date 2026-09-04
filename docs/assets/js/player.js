// Custom play/pause/scrub UI for each stop's ".audio-player" widget.
// Nothing here is stop-specific — it just wires up whatever markup
// build.py generated for that stop's audio_url.
(function () {
  function formatTime(seconds) {
    if (!isFinite(seconds)) return "0:00";
    var m = Math.floor(seconds / 60);
    var s = Math.floor(seconds % 60);
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  function setUp(root) {
    var audio = root.querySelector(".player-audio");
    var toggleBtn = root.querySelector(".player-toggle");
    var iconPlay = root.querySelector(".icon-play");
    var iconPause = root.querySelector(".icon-pause");
    var seek = root.querySelector(".player-seek");
    var curEl = root.querySelector(".player-time-current");
    var durEl = root.querySelector(".player-time-duration");
    var muteBtn = root.querySelector(".player-mute");
    var iconVolume = root.querySelector(".icon-volume");
    var iconMuted = root.querySelector(".icon-muted");
    var scrubbing = false;

    function updateFill() {
      var max = parseFloat(seek.max) || 0;
      var pct = max > 0 ? (seek.value / max) * 100 : 0;
      seek.style.background =
        "linear-gradient(to right, var(--orange) " + pct + "%, #ddd2c2 " + pct + "%)";
    }

    audio.addEventListener("loadedmetadata", function () {
      seek.max = audio.duration || 0;
      durEl.textContent = formatTime(audio.duration);
      updateFill();
    });

    audio.addEventListener("timeupdate", function () {
      if (!scrubbing) seek.value = audio.currentTime;
      curEl.textContent = formatTime(audio.currentTime);
      updateFill();
    });

    audio.addEventListener("ended", function () {
      iconPlay.hidden = false;
      iconPause.hidden = true;
      toggleBtn.setAttribute("aria-label", "Play");
    });

    toggleBtn.addEventListener("click", function () {
      if (audio.paused) {
        audio.play();
        iconPlay.hidden = true;
        iconPause.hidden = false;
        toggleBtn.setAttribute("aria-label", "Pause");
      } else {
        audio.pause();
        iconPlay.hidden = false;
        iconPause.hidden = true;
        toggleBtn.setAttribute("aria-label", "Play");
      }
    });

    seek.addEventListener("input", function () {
      scrubbing = true;
      audio.currentTime = seek.value;
      curEl.textContent = formatTime(audio.currentTime);
      updateFill();
    });
    seek.addEventListener("change", function () {
      scrubbing = false;
    });

    muteBtn.addEventListener("click", function () {
      audio.muted = !audio.muted;
      iconVolume.hidden = audio.muted;
      iconMuted.hidden = !audio.muted;
      muteBtn.setAttribute("aria-label", audio.muted ? "Unmute" : "Mute");
    });

    updateFill();
  }

  document.querySelectorAll(".audio-player").forEach(setUp);
})();

<style>
  .check-circle {
    width: 6.5rem;
    height: 6.5rem;
    background-color: #00a8e3;
    border-radius: 50%;
    display: block;
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    position: relative;
    animation: circleScale 0.5s ease 1;
    animation-timing-function: cubic-bezier(0.42, 0.97, 0.52, 1.49);
    margin: 3rem auto;
  }
  .check-circle__mark {
    display: block;
  }
  .check-circle__mark:after {
    position: absolute;
    top: 3.25rem;
    left: 1.45rem;
    transform: translate(0, 0);
    content: "";
    opacity: 0;
    height: 3.25rem;
    width: 1.75rem;
    border-right: 3px solid #fff;
    border-top: 3px solid #fff;
    transform-origin: left top;
    animation-delay: 0.6s;
    animation-duration: 900ms;
    animation-name: checkmark;
    transform: scaleX(-1) rotate(135deg);
    animation-timing-function: cubic-bezier(0.42, 0.97, 0.52, 1.49);
    animation-fill-mode: forwards;
  }

  @keyframes circleScale {
    0% {
      opacity: 0;
      transform: scale(0.5);
    }
    50% {
      transform: scale(1.1);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }
  @keyframes checkmark {
    0% {
      height: 0;
      width: 0;
      opacity: 0;
    }
    20% {
      height: 0;
      width: 1.75rem;
      opacity: 1;
    }
    40% {
      height: 3.25rem;
      width: 1.75rem;
      opacity: 1;
    }
    100% {
      height: 3.25rem;
      width: 1.75rem;
      opacity: 1;
    }
  }
</style>

<div class="check-circle">
  <div class="check-circle__mark" />
</div>

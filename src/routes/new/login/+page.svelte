<script>
  import Button from "../../../components/Button.svelte";
  import GoogleIcon from "../../../assets/icons/google.svg";
  import MicrosoftIcon from "../../../assets/icons/microsoft.svg";
</script>

<div class="py-[154px] pl-[192px] pr-[120px] flex items-start gap-[200px]">
  <div class="flex flex-col gap-[40px] items-start mt-[164px]">
    <div class="flex flex-col items-start gap-6 max-w-[768px]">
      <h1 class="font-bold text-5xl leading-[58px] tracking-[1.7px]">
        Pass your technical certification exam in <span
          class="text-primary-500"
        >
          record time
        </span>
      </h1>
      <p class="font-medium text-2xl leading-[29px] tracking-wide">
        Through retrieval training and hands-free functionality, DeckHub equips
        you with the tools to earn technical certifications faster than ever.
      </p>
    </div>
  </div>

  <div
    class="w-[640px] aspect-square p-[124px] rounded-4xl bg-[rgba(17,24,39,0.75)] flex flex-col items-center justify-center gap-[80px]"
  >
    <div class="text-white text-center w-full">
      <h3 class="text-4xl font-bold mb-10">Login</h3>
      <p class=" leading-[20px]">
        Link your account below to fully access DeckHub.
      </p>
    </div>

    <div class="flex flex-col gap-3 items-center w-full">
      <Button
        variant="primary-blue"
        className="w-[320px] gap-2 min-h-[58px] !text-base !font-semibold"
        >Sign-in with Microsoft
        <figure>
          <img src={MicrosoftIcon} alt="microsoft" width="26" height="26" />
        </figure>
      </Button>
      <span>Or</span>
      <Button
        variant="primary-blue"
        className="w-[320px] gap-2 min-h-[58px] !text-base !font-semibold"
        >Sign-in with Google <figure>
          <img src={GoogleIcon} alt="google" width="26" height="26" />
        </figure></Button
      >
    </div>
  </div>
</div>

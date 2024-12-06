<script lang="ts">
  import ConceptCard from "../routes/new/learn/[slug]/overview/ConceptCard.svelte";

  interface Concept {
    id: number;
    isCompleted: boolean;
    title: string;
  }

  export let TERMS_LIST: Concept[] = [];
  export let isChat: boolean = false;
  export let onStudyClick;

  const acronyms = {
    "scp": "SCP",
    "iam": "IAM",
    "dns": "DNS",
    "s3": "S3",
    "ec2": "EC2",
    "eip": "EIP",
    "asg": "ASG",
    "rpo": "RPO",
    "rto": "RTO",
    "ml": "ML",
    "cidr": "CIDR",
    "ip": "IP",
    "nacl": "NACL",
    "vpc": "VPC",
    "nat": "NAT",
    "ips": "IPS",
    "aws": "AWS",
    "cloudformation": "CloudFormation",
  };

  function formatTitle(inputString) {
    if (inputString.endsWith('_question')) {
      inputString = inputString.slice(0, -9);
    }

    return inputString
      .split('_')
      .map(word => {
        const lowerCaseWord = word.toLowerCase();
        if (acronyms[lowerCaseWord]) {
          return acronyms[lowerCaseWord];
        }
        return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
      })
      .join(' ');
  }
</script>

<div class="flex flex-col gap-10">
  <!-- Remaining Concepts -->
  <div class="flex flex-col gap-4">
    <h4 class="font-bold" style="font-size: {isChat ? '16px' : '12px'};">
      Remaining Concepts / Terms
    </h4>
    <div class="grid max-sm:grid-cols-1 grid-cols-2 gap-x-4 gap-y-3">
      {#each TERMS_LIST.filter((concept) => !concept.isCompleted) as concept (concept.id)}
        <ConceptCard
          isCompleted={false}
          title={formatTitle(concept.title)}
          isChat={isChat}
          onStudyClick={() => onStudyClick(concept.title)} 
        />
      {/each}
    </div>
  </div>

  <!-- Completed Concepts -->
  <div class="flex flex-col gap-4">
    <h4 class="font-bold" style="font-size: {isChat ? '16px' : '12px'};">
      Completed Concepts / Terms
    </h4>
    <div class="grid max-sm:grid-cols-1 grid-cols-2 gap-x-4 gap-y-3">
      {#each TERMS_LIST.filter((concept) => concept.isCompleted) as concept (concept.id)}
        <ConceptCard
          isCompleted={true}
          title={formatTitle(concept.title)}
          isChat={isChat}
        />
      {/each}
    </div>
  </div>
</div>

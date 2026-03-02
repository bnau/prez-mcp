<script setup lang="ts">
import SlideHeader from '../components/SlideHeader.vue'
import ContactLink from '../components/ContactLink.vue'

const props = defineProps<{
  section?: string
  sectionName?: string
  slideName?: string
  name: string
  jobTitle: string
  photo: string
  email: string
  linkedin: string
  github: string
  bluesky: string
  website: string
}>()

const emailIcon = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>'

const linkedinIcon = '<svg fill="#0A66C2" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'

const githubIcon = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>'

const blueskyIcon = '<svg fill="#0085FF" viewBox="0 0 568 501"><path d="M123.121 33.6637C188.241 82.5526 258.281 181.681 284 234.873C309.719 181.681 379.759 82.5526 444.879 33.6637C491.866 -1.61183 568 -28.9064 568 57.9464C568 75.2916 558.055 203.659 552.222 224.501C531.947 296.954 458.067 315.434 392.347 304.249C507.222 323.8 536.444 388.56 473.333 453.32C353.473 576.312 301.061 422.461 287.631 383.039C285.169 375.812 284.017 372.431 284 375.306C283.983 372.431 282.831 375.812 280.369 383.039C266.939 422.461 214.527 576.312 94.6667 453.32C31.5556 388.56 60.7778 323.8 175.653 304.249C109.933 315.434 36.0535 296.954 15.7778 224.501C9.94525 203.659 0 75.2916 0 57.9464C0 -28.9064 76.1345 -1.61183 123.121 33.6637Z"/></svg>'

const websiteIcon = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>'
</script>

<template>
  <div class="slidev-layout presentation h-full flex flex-col">
    <!-- Header -->
    <div class="flex-shrink-0">
      <SlideHeader
        :section="section"
        :sectionName="sectionName"
        :slideName="slideName"
      />
    </div>

    <!-- Content centré verticalement -->
    <div class="flex-1 flex items-center justify-center">
      <div class="w-full px-16">
        <div class="grid grid-cols-2 gap-16 w-full items-center">
          <!-- Colonne gauche : Photo et nom -->
          <div class="flex flex-col items-center">
            <img :src="photo" class="w-40 h-40 rounded-full mb-4" :alt="name" />
            <div class="text-center">
              <p class="text-2xl font-bold">{{ name }}</p>
              <p class="text-lg text-gray-600">{{ jobTitle }}</p>
            </div>
          </div>

          <!-- Colonne droite : Liens sociaux -->
          <div class="flex flex-col justify-center">
            <div class="text-sm space-y-3">
              <ContactLink
                :href="`mailto:${email}`"
                :icon="emailIcon"
                :label="email"
              />

              <ContactLink
                :href="`https://www.linkedin.com/in/${linkedin}`"
                :icon="linkedinIcon"
                :label="linkedin"
              />

              <ContactLink
                :href="`https://github.com/${github}`"
                :icon="githubIcon"
                :label="github"
              />

              <ContactLink
                :href="`https://bsky.app/profile/${bluesky}`"
                :icon="blueskyIcon"
                :label="`@${bluesky}`"
              />

              <ContactLink
                :href="`https://${website}`"
                :icon="websiteIcon"
                :label="website"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

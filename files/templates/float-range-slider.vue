<template>
<v-range-slider
  v-model="value"
  :label="label"
  :min="min" :max="max" :step="step"
  hide-details
  class="align-center"
>
  <template v-slot:append>
    <v-text-field
      type="number"
      :value="value[0]"
      :min="min" :max="max" :step="step"
      dense hide-details outlined single-line
      class="mt-0 pt-0"
      style="width: 5em"
      @change="$set(value, 0, $event)"
    ></v-text-field>
    <v-text-field
      type="number"
      :value="value[1]"
      :min="min" :max="max" :step="step"
      dense hide-details outlined single-line
      class="mt-0 pt-0"
      style="width: 5em"
      @change="$set(value, 1, $event)"
    ></v-text-field>
    <v-tooltip right v-if="resettable">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          fab
          small
          elevation="0"
          v-bind="attrs"
          v-on="on"
          @click="reset"
        >
          <v-icon>
            mdi-arrow-expand-horizontal
          </v-icon>
        </v-btn>
      </template>
      <span>reset</span>
    </v-tooltip>
  </template>
</v-range-slider>
</template>

<script>
module.exports = {
  methods: {
    reset() {
      this.value = [this.min, this.max];
    },
  },
};
</script>

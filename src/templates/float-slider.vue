<v-slider
  v-model="value"
  :label="label"
  :min="min" :max="max" :step="step"
  hide-details
  style="width: 400px"
  class="align-center"
>
  <template v-slot:append>
    <v-text-field
      v-model="value"
      type="number"
      :min="min" :step="step"
      dense hide-details outlined single-line
      class="mt-0 pt-0"
      style="width: 5em"
      @change="$set(value, $event)"
    ></v-text-field>
  </template>
</v-slider>

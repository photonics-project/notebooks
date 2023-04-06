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
      :min="min" :step="step"
      dense hide-details outlined single-line
      class="mt-0 pt-0"
      style="width: 5em"
      @change="$set(value, 0, $event)"
    ></v-text-field>
    <v-text-field
      type="number"
      :value="value[1]"
      :max="max" :step="step"
      dense hide-details outlined single-line
      class="mt-0 pt-0"
      style="width: 5em"
      @change="$set(value, 1, $event)"
    ></v-text-field>
  </template>
</v-range-slider>

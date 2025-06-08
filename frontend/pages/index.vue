<template>
  <div class="min-h-screen bg-walandoo-secondary font-sans">
    <header class="bg-walandoo-primary text-white py-6 px-4 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <img src="/walandoo-logo.svg" alt="Walandoo Logo" class="h-10 w-auto" />
        <span class="text-2xl font-bold tracking-tight">Walandoo</span>
      </div>
      <nav>
        <NuxtLink to="/cart" class="text-walandoo-accent font-semibold hover:underline">Cart</NuxtLink>
      </nav>
    </header>
    <main class="max-w-6xl mx-auto py-10 px-4">
      <h1 class="text-3xl font-bold text-walandoo-primary mb-6">Shop by Category</h1>
      <div v-if="categories.length" class="flex flex-wrap gap-3 mb-10">
        <button
          v-for="cat in categories"
          :key="cat"
          @click="selectedCategory = cat"
          :class="[
            'px-4 py-2 rounded-xl font-semibold transition',
            selectedCategory === cat ? 'bg-walandoo-accent text-white' : 'bg-white text-walandoo-primary border border-walandoo-gray hover:bg-walandoo-gray/30'
          ]"
        >
          {{ cat }}
        </button>
        <button
          @click="selectedCategory = ''"
          :class="[
            'px-4 py-2 rounded-xl font-semibold transition',
            selectedCategory === '' ? 'bg-walandoo-accent text-white' : 'bg-white text-walandoo-primary border border-walandoo-gray hover:bg-walandoo-gray/30'
          ]"
        >
          All
        </button>
      </div>
      <div v-if="loading" class="text-walandoo-primary">Loading products...</div>
      <div v-else-if="filteredProducts.length === 0" class="text-walandoo-primary">No products found.</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
        <div v-for="product in filteredProducts" :key="product.id" class="bg-white rounded-xl shadow p-4 flex flex-col">
          <img :src="product.image" :alt="product.title" class="h-48 w-full object-contain mb-4 rounded" />
          <h2 class="text-lg font-bold text-walandoo-primary mb-1">{{ product.title }}</h2>
          <div class="text-walandoo-gray text-sm mb-2">{{ product.category }}</div>
          <div class="text-walandoo-primary font-semibold text-xl mb-2">${{ product.price }}</div>
          <div class="flex-1 text-sm text-walandoo-primary mb-2">{{ product.description }}</div>
          <NuxtLink :to="`/product/${product.id}`" class="mt-auto bg-walandoo-accent text-white px-4 py-2 rounded-xl font-semibold text-center hover:bg-walandoo-primary transition">View Details</NuxtLink>
        </div>
      </div>
    </main>
    <footer class="bg-walandoo-primary text-white py-4 text-center mt-10">
      &copy; {{ new Date().getFullYear() }} Walandoo. All rights reserved.
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useFetch } from '#app'

const products = ref([])
const loading = ref(true)
const categories = ref([])
const selectedCategory = ref('')

onMounted(async () => {
  try {
    const { data, error } = await useFetch('/api/products/')
    if (error.value) throw error.value
    products.value = data.value || []
    categories.value = [...new Set(products.value.map(p => p.category))].sort()
  } catch (e) {
    // handle error (could show a toast or message)
    products.value = []
    categories.value = []
  } finally {
    loading.value = false
  }
})

const filteredProducts = computed(() => {
  if (!selectedCategory.value) return products.value
  return products.value.filter(p => p.category === selectedCategory.value)
})
</script>

<style scoped>
body {
  background: #F5F6FA;
}
</style>

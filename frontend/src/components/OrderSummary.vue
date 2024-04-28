<template>
    <div class="box mb-4">
        <h3 class="is-size-4 mb-6">Pedido #{{ order.id }}</h3>

        <h4 class="is-size-5">Produto</h4>

        <table class="table is-fullwidth">
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Preço</th>
                    <th>Quantidade</th>
                    <th>Total</th>
                </tr>
            </thead>

            <tbody>
                <tr
                    v-for="item in order.items"
                    v-bind:key="item.produto.id"
                >
                    <td>{{ item.produto.nome }}</td>
                    <td>${{ item.produto.preco }}</td>
                    <td>{{ item.quantidade }}</td>
                    <td>${{ getItemTotal(item).toFixed(2) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    name: 'OrderSummary',
    props: {
        order: Object
    },
    methods: {
        getItemTotal(item) {
            return item.quantidade * item.produto.preco
        },
        orderTotalLength(order) {
            return order.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
    }
}
</script>
public with sharing class InvoiceService {
    public static Decimal normalizeAmount(Decimal amount) {
        return amount == null ? 0 : amount.setScale(2);
    }
}

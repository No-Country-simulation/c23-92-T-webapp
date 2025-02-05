export default function formatDate(dateString: string): string {
    const options: Intl.DateTimeFormatOptions = {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
    };
    const date = new Date(dateString);
    return date.toLocaleDateString("es-ES", options);
}
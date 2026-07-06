<?php
/**
 * Ocean City PAT Testing — contact form handler.
 *
 * Receives the /contact "Request a quote" form, filters spam, and emails the
 * enquiry to sales@oceancitypattesting.co.uk. No third-party service, no CAPTCHA.
 *
 * Spam defences:
 *   1. Honeypot ("company_url") — hidden from humans; if filled, silently drop.
 *   2. Time-trap — JS reports elapsed ms since page load; <3s means a bot.
 *   3. Header-injection guard — CR/LF stripped from every header field.
 *   4. Link-spam heuristic — messages stuffed with URLs are dropped.
 * Bots are always shown "success" so they get no useful signal.
 */

const RECIPIENT = 'sales@oceancitypattesting.co.uk';
const MAIL_FROM  = 'noreply@oceancitypattesting.co.uk';
const CONTACT    = '/contact';

// --- helpers ---------------------------------------------------------------
function go($qs) {
    header('Location: ' . CONTACT . $qs, true, 303);
    exit;
}
function clean($v) {                                  // trim + strip control chars
    $v = is_string($v) ? trim($v) : '';
    return preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/u', '', $v);
}
function oneline($v) {                                // header-safe: never any CR/LF
    return str_replace(["\r", "\n", "\t"], ' ', clean($v));
}

// --- only accept POST ------------------------------------------------------
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    go('');
}

// --- 1. honeypot -----------------------------------------------------------
if (!empty($_POST['company_url'])) {
    go('?sent=1#request-a-quote');                    // pretend success, send nothing
}

// --- 2. time-trap (client-measured elapsed, so no server-clock skew) -------
if (isset($_POST['elapsed_ms']) && $_POST['elapsed_ms'] !== '') {
    $elapsed = (int) $_POST['elapsed_ms'];
    if ($elapsed >= 0 && $elapsed < 3000) {           // filled in under 3s = bot
        go('?sent=1#request-a-quote');
    }
}

// --- gather + validate -----------------------------------------------------
$name    = oneline($_POST['name']          ?? '');
$phone   = oneline($_POST['phone']         ?? '');
$email   = oneline($_POST['email']         ?? '');
$ptype   = oneline($_POST['property_type'] ?? '');
$area    = oneline($_POST['area']          ?? '');
$message = clean($_POST['message']         ?? '');    // body only — may be multi-line

$errors = [];
if ($name === ''  || mb_strlen($name)  > 100) $errors[] = 'name';
if ($phone === '' || mb_strlen($phone) > 40)  $errors[] = 'phone';
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($email) > 150) $errors[] = 'email';

// --- 4. link-spam heuristic ------------------------------------------------
$haystack = $name . ' ' . $message;
$links = preg_match_all('~https?://|www\.|\[url~i', $haystack);
if ($links >= 3 || preg_match('~\b(viagra|casino|bitcoin|crypto|airdrop|seo\s+services|backlinks)\b~i', $haystack)) {
    go('?sent=1#request-a-quote');                    // silently drop
}

if ($errors) {
    go('?error=1#request-a-quote');
}

// --- build + send ----------------------------------------------------------
$subject = 'New PAT enquiry — ' . ($name !== '' ? $name : 'website');

$body  = "New enquiry from the Ocean City PAT Testing website\n";
$body .= str_repeat('-', 50) . "\n\n";
$body .= "Name:          $name\n";
$body .= "Phone:         $phone\n";
$body .= "Email:         $email\n";
$body .= 'Property type: ' . ($ptype !== '' ? $ptype : '—') . "\n";
$body .= 'Area / town:   ' . ($area  !== '' ? $area  : '—') . "\n\n";
$body .= "Message:\n" . ($message !== '' ? $message : '(none provided)') . "\n\n";
$body .= str_repeat('-', 50) . "\n";
$body .= 'Sent: ' . date('D j M Y, H:i') . ' · IP ' . ($_SERVER['REMOTE_ADDR'] ?? '?') . "\n";

$replyName = str_replace(['<', '>', '"'], '', $name);
$headers  = 'From: Ocean City PAT Testing <' . MAIL_FROM . ">\r\n";
$headers .= 'Reply-To: ' . ($replyName !== '' ? $replyName . ' ' : '') . '<' . $email . ">\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "X-Mailer: OceanCity-Contact\r\n";

$ok = @mail(RECIPIENT, oneline($subject), $body, $headers, '-f' . MAIL_FROM);

go($ok ? '?sent=1#request-a-quote' : '?error=1#request-a-quote');

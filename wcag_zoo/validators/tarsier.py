from wcag_zoo.utils import WCAGCommand


class Tarsier(WCAGCommand):
    """
    Tarsier reads heading levels in HTML documents (H1,H2,...H6) to verfiy order and completion against the requirements of the WCAG2.0 standard
    """

    animal = """
        The tarsiers are prosimian (non-monkey) primates. They got their name from the long bones in their feet.
        They are now placed in the suborder Haplorhini, together with the simians (monkeys).

        Tarsiers have huge eyes and long feet, and catch the insects by jumping at them.
        During the night they wait quietly, listening for the sound of an insect moving nearby.

        - https://simple.wikipedia.org/wiki/Tarsier
    """

    xpath = '/html/body//*[%s]' % (" or ".join(['self::h%d' % x for x in range(7)]))

    error_codes = {
        1: "Incorrect header found at {elem} - H{bad} should be H{good}",
    }

    def run_validation_loop(self, xpath=None, validator=None):
        if xpath is None:
            xpath = self.xpath
        headers = []
        for node in self.tree.xpath(xpath):
            if self.check_skip_element(node):
                continue
            depth = int(node.tag[1])
            headers.append(depth)
        depth = 0
        for node in self.tree.xpath(xpath):
            h = int(node.tag[1])
            if h == depth:
                self.success += 1
            elif h == depth + 1:
                self.success += 1
            elif h < depth:
                self.success += 1
            else:
                self.add_failure(
                    guideline='1.3.1',
                    technique='G20',
                    node=node,
                    message=Tarsier.error_codes[1].format(
                        elem=node.getroottree().getpath(node),
                        good=depth,
                        bad=h
                    ),
                    error_code=1
                )
            depth = h

if __name__ == "__main__":
    cli = Tarsier.as_cli()
    cli()